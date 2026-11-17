from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.blog_repo import BlogRepository
from app.services.blog_cms_service import BlogCMSService
from app.schemas.blog import BlogResponse

router = APIRouter(prefix="/public/blogs", tags=["Public CMS - Blogs"])


def get_cms_service(db: AsyncSession = Depends(get_db)) -> BlogCMSService:
    return BlogCMSService(BlogRepository(db))


@router.get("", response_model=list[BlogResponse])
async def list_blogs(
    tag: str | None = Query(None, description="Filter by tag"),
    service: BlogCMSService = Depends(get_cms_service),
):
    return await service.list_public_blogs(tag=tag)


@router.get("/{slug}", response_model=BlogResponse)
async def get_blog_detail(
    slug: str,
    service: BlogCMSService = Depends(get_cms_service),
):
    return await service.get_public_blog_by_slug(slug)

