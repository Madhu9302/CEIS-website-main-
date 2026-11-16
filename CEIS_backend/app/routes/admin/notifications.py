import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.notification_repo import NotificationRepository
from app.services.notification_service import NotificationService
from app.schemas.notification import NotificationResponse, NotificationUpdate
from app.core.security import get_current_admin
from app.models.user import User

router = APIRouter(prefix="/admin/notifications", tags=["Admin Alerts"])

def get_notification_service(db: AsyncSession = Depends(get_db)) -> NotificationService:
    return NotificationService(NotificationRepository(db))

@router.get("", response_model=list[NotificationResponse])
async def list_notifications(
    _: User = Depends(get_current_admin),
    service: NotificationService = Depends(get_notification_service)
):
    return await service.get_notifications()

@router.patch("/{id}", response_model=NotificationResponse)
async def update_notification(
    id: uuid.UUID,
    payload: NotificationUpdate,
    _: User = Depends(get_current_admin),
    service: NotificationService = Depends(get_notification_service)
):
    return await service.mark_notification(id, payload)