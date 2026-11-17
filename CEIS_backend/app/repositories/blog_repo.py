import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.blog import Blog


class BlogRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, published_only: bool = False, tag: str | None = None) -> list[Blog]:
        stmt = select(Blog).order_by(Blog.published_at.desc().nullslast(), Blog.created_at.desc())
        if published_only:
            stmt = stmt.where(Blog.is_published.is_(True))
        if tag:
            stmt = stmt.where(Blog.tags.ilike(f"%{tag}%"))
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, blog_id: uuid.UUID) -> Blog | None:
        result = await self.db.execute(select(Blog).where(Blog.id == blog_id))
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str, published_only: bool = True) -> Blog | None:
        stmt = select(Blog).where(Blog.slug == slug)
        if published_only:
            stmt = stmt.where(Blog.is_published.is_(True))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, blog: Blog) -> Blog:
        self.db.add(blog)
        await self.db.commit()
        await self.db.refresh(blog)
        return blog

    async def update(self, blog: Blog, updates: dict) -> Blog:
        for key, value in updates.items():
            setattr(blog, key, value)
        await self.db.commit()
        await self.db.refresh(blog)
        return blog

    async def delete(self, blog: Blog) -> None:
        await self.db.delete(blog)
        await self.db.commit()

