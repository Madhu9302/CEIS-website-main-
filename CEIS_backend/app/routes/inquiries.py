import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.models.client_inquiry import ClientInquiry, generate_inquiry_reference_id
from app.schemas.client_inquiry import (
    ClientInquiryCreate,
    ClientInquiryCreateResponse,
    ClientInquiryStatusUpdate,
    ClientInquiryResponse,
)
from app.core.security import get_current_admin

router = APIRouter(prefix="/inquiries", tags=["Client Inquiries"])


@router.post("", response_model=ClientInquiryCreateResponse, status_code=status.HTTP_201_CREATED)
async def submit_inquiry(
    payload: ClientInquiryCreate,
    db: AsyncSession = Depends(get_db),
):
    # Ensure unique reference_id
    ref_id = generate_inquiry_reference_id()
    while True:
        existing = await db.execute(select(ClientInquiry).where(ClientInquiry.reference_id == ref_id))
        if not existing.scalar_one_or_none():
            break
        ref_id = generate_inquiry_reference_id()

    inquiry = ClientInquiry(
        reference_id=ref_id,
        full_name=payload.full_name,
        email=str(payload.email),
        company=payload.company,
        service_interest=payload.service_interest,
        message=payload.message,
        status="new",
    )
    db.add(inquiry)
    await db.commit()
    await db.refresh(inquiry)

    return ClientInquiryCreateResponse(
        reference_id=inquiry.reference_id,
        status=inquiry.status,
        created_at=inquiry.created_at,
    )


@router.get("", response_model=list[ClientInquiryResponse])
async def list_inquiries(
    _: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(ClientInquiry).order_by(ClientInquiry.created_at.desc())
    res = await db.execute(stmt)
    return list(res.scalars().all())


@router.patch("/{id}", response_model=ClientInquiryResponse)
async def update_inquiry_status(
    id: str,
    payload: ClientInquiryStatusUpdate,
    _: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(ClientInquiry)
    try:
        val_uuid = uuid.UUID(id)
        stmt = stmt.where((ClientInquiry.id == val_uuid) | (ClientInquiry.reference_id == id))
    except ValueError:
        stmt = stmt.where(ClientInquiry.reference_id == id)

    res = await db.execute(stmt)
    inquiry = res.scalar_one_or_none()
    if not inquiry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inquiry not found")

    inquiry.status = payload.status
    await db.commit()
    await db.refresh(inquiry)
    return inquiry
