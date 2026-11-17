import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class SiteSettingBase(BaseModel):
    key: str = Field(..., min_length=1, max_length=100)
    value: str
    description: str | None = None


class SiteSettingCreate(SiteSettingBase):
    model_config = ConfigDict(extra="forbid")


class SiteSettingUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    value: str | None = None
    description: str | None = None


class SiteSettingResponse(SiteSettingBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    updated_at: datetime

