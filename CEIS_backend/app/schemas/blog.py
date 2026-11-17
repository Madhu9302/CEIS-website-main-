import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class BlogBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    slug: str = Field(..., min_length=2, max_length=280)
    excerpt: str | None = None
    content: str = Field(..., min_length=5)
    cover_image: str | None = None
    author_name: str | None = None
    tags: str | None = None
    is_published: bool = False
    published_at: datetime | None = None


class BlogCreate(BlogBase):
    model_config = ConfigDict(extra="forbid")


class BlogUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(None, min_length=2, max_length=255)
    slug: str | None = Field(None, min_length=2, max_length=280)
    excerpt: str | None = None
    content: str | None = Field(None, min_length=5)
    cover_image: str | None = None
    author_name: str | None = None
    tags: str | None = None
    is_published: bool | None = None
    published_at: datetime | None = None


class BlogResponse(BlogBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

