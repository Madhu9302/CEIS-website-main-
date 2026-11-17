from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.job_repo import JobRepository
from app.services.job_cms_service import JobCMSService
from app.schemas.job import JobResponse, JobApplicationCreate, JobApplicationResponse

router = APIRouter(prefix="/public/jobs", tags=["Public CMS - Jobs"])


def get_cms_service(db: AsyncSession = Depends(get_db)) -> JobCMSService:
    return JobCMSService(JobRepository(db))


@router.get("", response_model=list[JobResponse])
async def list_jobs(
    department: str | None = Query(None, description="Filter by department"),
    service: JobCMSService = Depends(get_cms_service),
):
    return await service.list_public_jobs(department=department)


@router.get("/{slug}", response_model=JobResponse)
async def get_job_detail(
    slug: str,
    service: JobCMSService = Depends(get_cms_service),
):
    return await service.get_public_job_by_slug(slug)


@router.post("/apply", response_model=JobApplicationResponse, status_code=status.HTTP_201_CREATED)
async def apply_job(
    payload: JobApplicationCreate,
    service: JobCMSService = Depends(get_cms_service),
):
    return await service.submit_application(payload)

