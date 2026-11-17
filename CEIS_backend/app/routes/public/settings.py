from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.site_setting_repo import SiteSettingRepository
from app.services.site_setting_cms_service import SiteSettingCMSService
from app.schemas.site_setting import SiteSettingResponse

router = APIRouter(prefix="/public/settings", tags=["Public CMS - Settings"])


def get_cms_service(db: AsyncSession = Depends(get_db)) -> SiteSettingCMSService:
    return SiteSettingCMSService(SiteSettingRepository(db))


@router.get("", response_model=list[SiteSettingResponse])
async def list_settings(service: SiteSettingCMSService = Depends(get_cms_service)):
    return await service.list_public_settings()


@router.get("/{key}", response_model=SiteSettingResponse)
async def get_setting(key: str, service: SiteSettingCMSService = Depends(get_cms_service)):
    return await service.get_setting_by_key(key)

