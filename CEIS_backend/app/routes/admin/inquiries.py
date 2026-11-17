import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.inquiry_repo import InquiryRepository
from app.services.inquiry_service import InquiryService
from app.schemas.inquiry import InquiryResponse, InquiryStatusUpdate
from app.core.permissions import get_current_admin
from app.models.user import User

router = APIRouter(prefix="/admin/inquiries", tags=["Admin CMS - Inquiries"])


def get_inquiry_service(db: AsyncSession = Depends(get_db)) -> InquiryService:
    return InquiryService(InquiryRepository(db))


@router.get("", response_model=list[InquiryResponse])
async def admin_list_inquiries(
    type: str | None = Query(None, description="Filter by type ('contact' or 'quote')"),
    status: str | None = Query(None, description="Filter by status ('new', 'in_progress', 'resolved', 'closed')"),
    _: User = Depends(get_current_admin),
    service: InquiryService = Depends(get_inquiry_service),
):
    return await service.list_inquiries(type=type, status=status)


@router.get("/{inquiry_id}", response_model=InquiryResponse)
async def admin_get_inquiry(
    inquiry_id: uuid.UUID,
    _: User = Depends(get_current_admin),
    service: InquiryService = Depends(get_inquiry_service),
):
    return await service.get_inquiry_by_id(inquiry_id)


@router.patch("/{inquiry_id}", response_model=InquiryResponse)
@router.patch("/{inquiry_id}/status", response_model=InquiryResponse)
async def admin_update_inquiry_status(
    inquiry_id: uuid.UUID,
    payload: InquiryStatusUpdate,
    _: User = Depends(get_current_admin),
    service: InquiryService = Depends(get_inquiry_service),
):
    return await service.update_inquiry_status(inquiry_id, payload)


@router.delete("/{inquiry_id}")
async def admin_delete_inquiry(
    inquiry_id: uuid.UUID,
    _: User = Depends(get_current_admin),
    service: InquiryService = Depends(get_inquiry_service),
):
    return await service.delete_inquiry(inquiry_id)

