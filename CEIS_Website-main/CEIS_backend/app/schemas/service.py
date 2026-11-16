import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ServiceBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    slug: str = Field(..., min_length=2, max_length=220)
    short_description: str = Field(..., min_length=5, max_length=500)
    description: str = Field(..., min_length=10)
    icon: str | None = None
    display_order: int = 0
    is_active: bool = True


class ServiceCreate(ServiceBase):
    model_config = ConfigDict(extra="forbid")


class ServiceUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(None, min_length=2, max_length=200)
    slug: str | None = Field(None, min_length=2, max_length=220)
    short_description: str | None = Field(None, min_length=5, max_length=500)
    description: str | None = Field(None, min_length=10)
    icon: str | None = None
    display_order: int | None = None
    is_active: bool | None = None


class ServiceResponse(ServiceBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime