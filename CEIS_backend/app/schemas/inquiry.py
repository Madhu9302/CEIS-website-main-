import uuid
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class InquiryStatusUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["new", "in_progress", "resolved", "closed"]


class InquiryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    type: str
    name: str
    email: str
    phone: str | None = None
    company: str | None = None
    service_interest: str | None = None
    budget_range: str | None = None
    message: str
    status: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

