import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.submission import Submission


class InquiryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, type: str | None = None, status: str | None = None) -> list[Submission]:
        stmt = select(Submission).where(Submission.is_deleted.is_(False)).order_by(Submission.created_at.desc())
        if type:
            stmt = stmt.where(Submission.type == type)
        if status:
            stmt = stmt.where(Submission.status == status)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, inquiry_id: uuid.UUID) -> Submission | None:
        stmt = select(Submission).where(Submission.id == inquiry_id, Submission.is_deleted.is_(False))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update_status(self, submission: Submission, status: str) -> Submission:
        submission.status = status
        await self.db.commit()
        await self.db.refresh(submission)
        return submission

    async def soft_delete(self, submission: Submission) -> None:
        submission.is_deleted = True
        await self.db.commit()

