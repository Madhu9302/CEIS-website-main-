import uuid
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ClientInquiryCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr = Field(..., max_length=160)
    company: str | None = Field(None, max_length=160)
    service_interest: str | None = Field(None, max_length=100)
    message: str = Field(..., min_length=2)


class ClientInquiryCreateResponse(BaseModel):
    reference_id: str
    status: str
    created_at: datetime


class ClientInquiryStatusUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["new", "in_review", "contacted", "archived"]


class ClientInquiryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    reference_id: str
    full_name: str
    email: str
    company: str | None = None
    service_interest: str | None = None
    message: str
    status: str
    created_at: datetime
