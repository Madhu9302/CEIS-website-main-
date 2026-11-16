import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class NotificationUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    is_read: bool = True

class NotificationResponse(BaseModel):
    id: uuid.UUID
    title: str
    message: str
    submission_id: uuid.UUID | None
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)     