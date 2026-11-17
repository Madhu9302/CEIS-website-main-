import uuid
from fastapi import HTTPException, status
from app.models.submission import Submission
from app.repositories.inquiry_repo import InquiryRepository
from app.schemas.inquiry import InquiryStatusUpdate

VALID_STATUSES = {"new", "in_progress", "resolved", "closed"}


class InquiryService:
    def __init__(self, repo: InquiryRepository):
        self.repo = repo

    async def list_inquiries(self, type: str | None = None, status: str | None = None) -> list[Submission]:
        return await self.repo.get_all(type=type, status=status)

    async def get_inquiry_by_id(self, inquiry_id: uuid.UUID) -> Submission:
        submission = await self.repo.get_by_id(inquiry_id)
        if not submission:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inquiry not found")
        return submission

    async def update_inquiry_status(self, inquiry_id: uuid.UUID, payload: InquiryStatusUpdate) -> Submission:
        submission = await self.repo.get_by_id(inquiry_id)
        if not submission:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inquiry not found")
        if payload.status not in VALID_STATUSES:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid status: {payload.status}")
        return await self.repo.update_status(submission, payload.status)

    async def delete_inquiry(self, inquiry_id: uuid.UUID) -> dict:
        submission = await self.repo.get_by_id(inquiry_id)
        if not submission:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inquiry not found")
        await self.repo.soft_delete(submission)
        return {"message": "Inquiry deleted successfully"}

