import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.blog_repo import BlogRepository
from app.services.blog_cms_service import BlogCMSService
from app.schemas.blog import BlogCreate, BlogUpdate, BlogResponse
from app.core.permissions import get_current_admin
from app.models.user import User

router = APIRouter(prefix="/admin/blogs", tags=["Admin CMS - Blogs"])


def get_cms_service(db: AsyncSession = Depends(get_db)) -> BlogCMSService:
    return BlogCMSService(BlogRepository(db))


@router.get("", response_model=list[BlogResponse])
async def admin_list_blogs(
    _: User = Depends(get_current_admin),
    service: BlogCMSService = Depends(get_cms_service),
):
    return await service.list_all_blogs()


@router.get("/{blog_id}", response_model=BlogResponse)
async def admin_get_blog(
    blog_id: uuid.UUID,
    _: User = Depends(get_current_admin),
    service: BlogCMSService = Depends(get_cms_service),
):
    return await service.get_blog_by_id(blog_id)


@router.post("", response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
async def admin_create_blog(
    payload: BlogCreate,
    _: User = Depends(get_current_admin),
    service: BlogCMSService = Depends(get_cms_service),
):
    return await service.create_blog(payload)


@router.patch("/{blog_id}", response_model=BlogResponse)
async def admin_update_blog(
    blog_id: uuid.UUID,
    payload: BlogUpdate,
    _: User = Depends(get_current_admin),
    service: BlogCMSService = Depends(get_cms_service),
):
    return await service.update_blog(blog_id, payload)


@router.delete("/{blog_id}")
async def admin_delete_blog(
    blog_id: uuid.UUID,
    _: User = Depends(get_current_admin),
    service: BlogCMSService = Depends(get_cms_service),
):
    return await service.delete_blog(blog_id)

