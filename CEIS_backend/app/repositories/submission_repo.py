from sqlalchemy.ext.asyncio import AsyncSession
from app.models.submission import Submission

class SubmissionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, submission: Submission) -> Submission:
        self.db.add(submission)
        await self.db.commit()
        await self.db.refresh(submission)
        return submission