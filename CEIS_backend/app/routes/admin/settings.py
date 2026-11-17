from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.site_setting_repo import SiteSettingRepository
from app.services.site_setting_cms_service import SiteSettingCMSService
from app.schemas.site_setting import SiteSettingCreate, SiteSettingUpdate, SiteSettingResponse
from app.core.permissions import get_current_admin
from app.models.user import User

router = APIRouter(prefix="/admin/settings", tags=["Admin CMS - Settings"])


def get_cms_service(db: AsyncSession = Depends(get_db)) -> SiteSettingCMSService:
    return SiteSettingCMSService(SiteSettingRepository(db))


@router.get("", response_model=list[SiteSettingResponse])
async def admin_list_settings(
    _: User = Depends(get_current_admin),
    service: SiteSettingCMSService = Depends(get_cms_service),
):
    return await service.list_all_settings()


@router.post("", response_model=SiteSettingResponse, status_code=status.HTTP_200_OK)
async def admin_upsert_setting(
    payload: SiteSettingCreate,
    _: User = Depends(get_current_admin),
    service: SiteSettingCMSService = Depends(get_cms_service),
):
    return await service.upsert_setting(payload)


@router.patch("/{key}", response_model=SiteSettingResponse)
async def admin_update_setting(
    key: str,
    payload: SiteSettingUpdate,
    _: User = Depends(get_current_admin),
    service: SiteSettingCMSService = Depends(get_cms_service),
):
    return await service.update_setting(key, payload)


@router.delete("/{key}")
async def admin_delete_setting(
    key: str,
    _: User = Depends(get_current_admin),
    service: SiteSettingCMSService = Depends(get_cms_service),
):
    return await service.delete_setting(key)

