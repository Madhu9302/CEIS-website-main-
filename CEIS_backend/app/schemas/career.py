import uuid
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CareerRoleBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=140)
    department: str = Field(..., min_length=2, max_length=80)
    location: str = Field(default="Indore, MP (On-Site / Hybrid)", max_length=120)
    employment_type: str = Field(default="Full-Time", max_length=50)
    experience: str | None = Field(None, max_length=60)
    description: str = Field(..., min_length=10)
    is_active: bool = True


class CareerRoleCreate(CareerRoleBase):
    model_config = ConfigDict(extra="forbid")


class CareerRoleResponse(CareerRoleBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


class JobApplicationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role_id: uuid.UUID | None = None
    role_title: str = Field(..., min_length=2, max_length=140)
    full_name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr = Field(..., max_length=160)
    phone: str = Field(..., min_length=3, max_length=30)
    portfolio_url: str = Field(..., min_length=3)
    resume_url: str = Field(..., min_length=3)
    cover_note: str | None = None


class JobApplicationCreateResponse(BaseModel):
    application_id: str
    status: str


class JobApplicationStatusUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["received", "shortlisted", "interviewing", "rejected"]


class JobApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    application_id: str
    role_id: uuid.UUID | None = None
    role_title: str
    full_name: str
    email: str
    phone: str
    portfolio_url: str
    resume_url: str
    cover_note: str | None = None
    status: str
    created_at: datetime
