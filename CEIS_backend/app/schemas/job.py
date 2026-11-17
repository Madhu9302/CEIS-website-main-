import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class JobBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    slug: str = Field(..., min_length=2, max_length=220)
    department: str = Field(..., min_length=2, max_length=100)
    location: str = Field(..., min_length=2, max_length=150)
    employment_type: str = Field(..., min_length=2, max_length=50)
    description: str = Field(..., min_length=10)
    requirements: str = Field(..., min_length=10)
    is_active: bool = True


class JobCreate(JobBase):
    model_config = ConfigDict(extra="forbid")


class JobUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(None, min_length=2, max_length=200)
    slug: str | None = Field(None, min_length=2, max_length=220)
    department: str | None = Field(None, min_length=2, max_length=100)
    location: str | None = Field(None, min_length=2, max_length=150)
    employment_type: str | None = Field(None, min_length=2, max_length=50)
    description: str | None = Field(None, min_length=10)
    requirements: str | None = Field(None, min_length=10)
    is_active: bool | None = None


class JobResponse(JobBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class JobApplicationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    job_id: uuid.UUID
    applicant_name: str = Field(..., min_length=2, max_length=200)
    email: EmailStr
    phone: str | None = Field(None, max_length=50)
    resume_url: str = Field(..., min_length=5, max_length=500)
    cover_letter: str | None = None


class JobApplicationStatusUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str = Field(..., min_length=2, max_length=50)


class JobApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    job_id: uuid.UUID
    applicant_name: str
    email: str
    phone: str | None = None
    resume_url: str
    cover_letter: str | None = None
    status: str
    created_at: datetime

