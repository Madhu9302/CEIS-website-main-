import uuid
from datetime import datetime, timezone
from fastapi import HTTPException, status
from app.models.blog import Blog
from app.repositories.blog_repo import BlogRepository
from app.schemas.blog import BlogCreate, BlogUpdate


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class BlogCMSService:
    def __init__(self, repo: BlogRepository):
        self.repo = repo

    async def list_public_blogs(self, tag: str | None = None) -> list[Blog]:
        return await self.repo.get_all(published_only=True, tag=tag)

    async def get_public_blog_by_slug(self, slug: str) -> Blog:
        blog = await self.repo.get_by_slug(slug, published_only=True)
        if not blog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
        return blog

    async def list_all_blogs(self) -> list[Blog]:
        return await self.repo.get_all(published_only=False)

    async def get_blog_by_id(self, blog_id: uuid.UUID) -> Blog:
        blog = await self.repo.get_by_id(blog_id)
        if not blog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
        return blog

    async def create_blog(self, payload: BlogCreate) -> Blog:
        existing = await self.repo.get_by_slug(payload.slug, published_only=False)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Blog slug already exists")
        data = payload.model_dump()
        if data.get("is_published") and not data.get("published_at"):
            data["published_at"] = utc_now()
        blog = Blog(**data)
        return await self.repo.create(blog)

    async def update_blog(self, blog_id: uuid.UUID, payload: BlogUpdate) -> Blog:
        blog = await self.repo.get_by_id(blog_id)
        if not blog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
        updates = payload.model_dump(exclude_unset=True)
        if "slug" in updates and updates["slug"] != blog.slug:
            existing = await self.repo.get_by_slug(updates["slug"], published_only=False)
            if existing:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Blog slug already exists")
        if updates.get("is_published") and not blog.published_at and not updates.get("published_at"):
            updates["published_at"] = utc_now()
        return await self.repo.update(blog, updates)

    async def delete_blog(self, blog_id: uuid.UUID) -> dict:
        blog = await self.repo.get_by_id(blog_id)
        if not blog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
        await self.repo.delete(blog)
        return {"message": "Blog deleted successfully"}

