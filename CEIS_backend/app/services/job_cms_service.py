import uuid
from fastapi import HTTPException, status
from app.models.job import Job, JobApplication
from app.repositories.job_repo import JobRepository
from app.schemas.job import JobCreate, JobUpdate, JobApplicationCreate, JobApplicationStatusUpdate


class JobCMSService:
    def __init__(self, repo: JobRepository):
        self.repo = repo

    async def list_public_jobs(self, department: str | None = None) -> list[Job]:
        return await self.repo.get_all_jobs(active_only=True, department=department)

    async def get_public_job_by_slug(self, slug: str) -> Job:
        job = await self.repo.get_job_by_slug(slug, active_only=True)
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
        return job

    async def submit_application(self, payload: JobApplicationCreate) -> JobApplication:
        job = await self.repo.get_job_by_id(payload.job_id)
        if not job or not job.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Active job not found")
        application = JobApplication(**payload.model_dump())
        return await self.repo.create_application(application)

    async def list_all_jobs(self) -> list[Job]:
        return await self.repo.get_all_jobs(active_only=False)

    async def get_job_by_id(self, job_id: uuid.UUID) -> Job:
        job = await self.repo.get_job_by_id(job_id)
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
        return job

    async def create_job(self, payload: JobCreate) -> Job:
        existing = await self.repo.get_job_by_slug(payload.slug, active_only=False)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Job slug already exists")
        job = Job(**payload.model_dump())
        return await self.repo.create_job(job)

    async def update_job(self, job_id: uuid.UUID, payload: JobUpdate) -> Job:
        job = await self.repo.get_job_by_id(job_id)
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
        updates = payload.model_dump(exclude_unset=True)
        if "slug" in updates and updates["slug"] != job.slug:
            existing = await self.repo.get_job_by_slug(updates["slug"], active_only=False)
            if existing:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Job slug already exists")
        return await self.repo.update_job(job, updates)

    async def delete_job(self, job_id: uuid.UUID) -> dict:
        job = await self.repo.get_job_by_id(job_id)
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
        await self.repo.delete_job(job)
        return {"message": "Job deleted successfully"}

    async def list_applications(
        self, job_id: uuid.UUID | None = None, status: str | None = None
    ) -> list[JobApplication]:
        return await self.repo.get_applications(job_id=job_id, status=status)

    async def get_application_by_id(self, application_id: uuid.UUID) -> JobApplication:
        application = await self.repo.get_application_by_id(application_id)
        if not application:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
        return application

    async def update_application_status(
        self, application_id: uuid.UUID, payload: JobApplicationStatusUpdate
    ) -> JobApplication:
        application = await self.repo.get_application_by_id(application_id)
        if not application:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
        return await self.repo.update_application_status(application, payload.status)

