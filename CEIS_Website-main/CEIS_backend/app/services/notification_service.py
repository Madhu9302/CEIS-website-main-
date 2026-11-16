import uuid
from fastapi import HTTPException, status
from app.repositories.notification_repo import NotificationRepository
from app.schemas.notification import NotificationUpdate
from app.models.notification import Notification

class NotificationService:
    def __init__(self, repo: NotificationRepository):
        self.repo = repo

    async def get_notifications(self) -> list[Notification]:
        return await self.repo.list_all()

    async def mark_notification(self, notif_id: uuid.UUID, data: NotificationUpdate) -> Notification:
        notif = await self.repo.get_by_id(notif_id)
        if not notif:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
        notif.is_read = data.is_read
        return await self.repo.update(notif)