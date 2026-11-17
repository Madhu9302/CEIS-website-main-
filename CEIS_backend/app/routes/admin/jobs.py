import uuid
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.job_repo import JobRepository
from app.services.job_cms_service import JobCMSService
from app.schemas.job import (
    JobCreate,
    JobUpdate,
    JobResponse,
    JobApplicationResponse,
    JobApplicationStatusUpdate,
)
from app.core.permissions import get_current_admin
from app.models.user import User

router = APIRouter(prefix="/admin/jobs", tags=["Admin CMS - Jobs"])


def get_cms_service(db: AsyncSession = Depends(get_db)) -> JobCMSService:
    return JobCMSService(JobRepository(db))


@router.get("", response_model=list[JobResponse])
async def admin_list_jobs(
    _: User = Depends(get_current_admin),
    service: JobCMSService = Depends(get_cms_service),
):
    return await service.list_all_jobs()


@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def admin_create_job(
    payload: JobCreate,
    _: User = Depends(get_current_admin),
    service: JobCMSService = Depends(get_cms_service),
):
    return await service.create_job(payload)


@router.get("/applications", response_model=list[JobApplicationResponse])
async def admin_list_applications(
    job_id: uuid.UUID | None = Query(None, description="Filter by job ID"),
    status: str | None = Query(None, description="Filter by application status"),
    _: User = Depends(get_current_admin),
    service: JobCMSService = Depends(get_cms_service),
):
    return await service.list_applications(job_id=job_id, status=status)


@router.patch("/applications/{application_id}/status", response_model=JobApplicationResponse)
async def admin_update_application_status(
    application_id: uuid.UUID,
    payload: JobApplicationStatusUpdate,
    _: User = Depends(get_current_admin),
    service: JobCMSService = Depends(get_cms_service),
):
    return await service.update_application_status(application_id, payload)


@router.get("/{job_id}", response_model=JobResponse)
async def admin_get_job(
    job_id: uuid.UUID,
    _: User = Depends(get_current_admin),
    service: JobCMSService = Depends(get_cms_service),
):
    return await service.get_job_by_id(job_id)


@router.patch("/{job_id}", response_model=JobResponse)
async def admin_update_job(
    job_id: uuid.UUID,
    payload: JobUpdate,
    _: User = Depends(get_current_admin),
    service: JobCMSService = Depends(get_cms_service),
):
    return await service.update_job(job_id, payload)


@router.delete("/{job_id}")
async def admin_delete_job(
    job_id: uuid.UUID,
    _: User = Depends(get_current_admin),
    service: JobCMSService = Depends(get_cms_service),
):
    return await service.delete_job(job_id)

