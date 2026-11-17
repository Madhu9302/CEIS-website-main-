import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.models.career import JobApplication, generate_application_id
from app.schemas.career import (
    JobApplicationCreate,
    JobApplicationCreateResponse,
    JobApplicationStatusUpdate,
    JobApplicationResponse,
)
from app.core.security import get_current_admin

router = APIRouter(prefix="/applications", tags=["Job Applications"])


@router.post("", response_model=JobApplicationCreateResponse, status_code=status.HTTP_201_CREATED)
async def submit_application(
    payload: JobApplicationCreate,
    db: AsyncSession = Depends(get_db),
):
    app_id = generate_application_id()
    while True:
        existing = await db.execute(select(JobApplication).where(JobApplication.application_id == app_id))
        if not existing.scalar_one_or_none():
            break
        app_id = generate_application_id()

    application = JobApplication(
        application_id=app_id,
        role_id=payload.role_id,
        role_title=payload.role_title,
        full_name=payload.full_name,
        email=str(payload.email),
        phone=payload.phone,
        portfolio_url=payload.portfolio_url,
        resume_url=payload.resume_url,
        cover_note=payload.cover_note,
        status="received",
    )
    db.add(application)
    await db.commit()
    await db.refresh(application)

    return JobApplicationCreateResponse(
        application_id=application.application_id,
        status=application.status,
    )


@router.get("", response_model=list[JobApplicationResponse])
async def list_applications(
    _: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(JobApplication).order_by(JobApplication.created_at.desc())
    res = await db.execute(stmt)
    return list(res.scalars().all())


@router.patch("/{id}", response_model=JobApplicationResponse)
async def update_application_status(
    id: str,
    payload: JobApplicationStatusUpdate,
    _: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(JobApplication)
    try:
        val_uuid = uuid.UUID(id)
        stmt = stmt.where((JobApplication.id == val_uuid) | (JobApplication.application_id == id))
    except ValueError:
        stmt = stmt.where(JobApplication.application_id == id)

    res = await db.execute(stmt)
    application = res.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    application.status = payload.status
    await db.commit()
    await db.refresh(application)
    return application
