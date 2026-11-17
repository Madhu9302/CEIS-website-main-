import uuid
from fastapi import HTTPException, status
from app.models.site_setting import SiteSetting
from app.repositories.site_setting_repo import SiteSettingRepository
from app.schemas.site_setting import SiteSettingCreate, SiteSettingUpdate


class SiteSettingCMSService:
    def __init__(self, repo: SiteSettingRepository):
        self.repo = repo

    async def list_public_settings(self) -> list[SiteSetting]:
        return await self.repo.get_all()

    async def list_all_settings(self) -> list[SiteSetting]:
        return await self.repo.get_all()

    async def get_setting_by_key(self, key: str) -> SiteSetting:
        setting = await self.repo.get_by_key(key)
        if not setting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Setting not found")
        return setting

    async def upsert_setting(self, payload: SiteSettingCreate) -> SiteSetting:
        setting = await self.repo.get_by_key(payload.key)
        if setting:
            updates = {"value": payload.value}
            if payload.description is not None:
                updates["description"] = payload.description
            return await self.repo.update(setting, updates)
        else:
            setting = SiteSetting(**payload.model_dump())
            return await self.repo.create(setting)

    async def update_setting(self, key: str, payload: SiteSettingUpdate) -> SiteSetting:
        setting = await self.repo.get_by_key(key)
        if not setting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Setting not found")
        updates = payload.model_dump(exclude_unset=True)
        return await self.repo.update(setting, updates)

    async def delete_setting(self, key: str) -> dict:
        setting = await self.repo.get_by_key(key)
        if not setting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Setting not found")
        await self.repo.delete(setting)
        return {"message": "Setting deleted successfully"}

