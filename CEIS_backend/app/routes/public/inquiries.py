from fastapi import APIRouter, Depends, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.submission_repo import SubmissionRepository
from app.repositories.notification_repo import NotificationRepository
from app.services.submission_service import SubmissionService
from app.schemas.submission import ContactRequest, QuoteRequest, PublicSubmissionResponse

router = APIRouter(prefix="/public", tags=["Public Inquiries"])

def get_submission_service(db: AsyncSession = Depends(get_db)) -> SubmissionService:
    return SubmissionService(SubmissionRepository(db), NotificationRepository(db))

@router.post("/contact", response_model=PublicSubmissionResponse, status_code=status.HTTP_201_CREATED)
async def submit_contact(
    payload: ContactRequest,
    bg_tasks: BackgroundTasks,
    service: SubmissionService = Depends(get_submission_service)
):
    return await service.submit_contact(payload, bg_tasks)

@router.post("/quote-req", response_model=PublicSubmissionResponse, status_code=status.HTTP_201_CREATED)
async def submit_quote(
    payload: QuoteRequest,
    bg_tasks: BackgroundTasks,
    service: SubmissionService = Depends(get_submission_service)
):
    return await service.submit_quote(payload, bg_tasks)