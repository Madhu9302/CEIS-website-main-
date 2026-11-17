import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.job import Job, JobApplication


class JobRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_jobs(self, active_only: bool = False, department: str | None = None) -> list[Job]:
        stmt = select(Job).order_by(Job.created_at.desc())
        if active_only:
            stmt = stmt.where(Job.is_active.is_(True))
        if department:
            stmt = stmt.where(Job.department.ilike(f"%{department}%"))
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_job_by_id(self, job_id: uuid.UUID) -> Job | None:
        result = await self.db.execute(select(Job).where(Job.id == job_id))
        return result.scalar_one_or_none()

    async def get_job_by_slug(self, slug: str, active_only: bool = True) -> Job | None:
        stmt = select(Job).where(Job.slug == slug)
        if active_only:
            stmt = stmt.where(Job.is_active.is_(True))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_job(self, job: Job) -> Job:
        self.db.add(job)
        await self.db.commit()
        await self.db.refresh(job)
        return job

    async def update_job(self, job: Job, updates: dict) -> Job:
        for key, value in updates.items():
            setattr(job, key, value)
        await self.db.commit()
        await self.db.refresh(job)
        return job

    async def delete_job(self, job: Job) -> None:
        await self.db.delete(job)
        await self.db.commit()

    async def create_application(self, application: JobApplication) -> JobApplication:
        self.db.add(application)
        await self.db.commit()
        await self.db.refresh(application)
        return application

    async def get_applications(
        self, job_id: uuid.UUID | None = None, status: str | None = None
    ) -> list[JobApplication]:
        stmt = select(JobApplication).order_by(JobApplication.created_at.desc())
        if job_id:
            stmt = stmt.where(JobApplication.job_id == job_id)
        if status:
            stmt = stmt.where(JobApplication.status == status)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_application_by_id(self, application_id: uuid.UUID) -> JobApplication | None:
        result = await self.db.execute(select(JobApplication).where(JobApplication.id == application_id))
        return result.scalar_one_or_none()

    async def update_application_status(self, application: JobApplication, status: str) -> JobApplication:
        application.status = status
        await self.db.commit()
        await self.db.refresh(application)
        return application

