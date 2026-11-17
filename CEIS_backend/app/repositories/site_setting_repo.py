import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.site_setting import SiteSetting


class SiteSettingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[SiteSetting]:
        result = await self.db.execute(select(SiteSetting).order_by(SiteSetting.key.asc()))
        return list(result.scalars().all())

    async def get_by_key(self, key: str) -> SiteSetting | None:
        result = await self.db.execute(select(SiteSetting).where(SiteSetting.key == key))
        return result.scalar_one_or_none()

    async def get_by_id(self, setting_id: uuid.UUID) -> SiteSetting | None:
        result = await self.db.execute(select(SiteSetting).where(SiteSetting.id == setting_id))
        return result.scalar_one_or_none()

    async def create(self, setting: SiteSetting) -> SiteSetting:
        self.db.add(setting)
        await self.db.commit()
        await self.db.refresh(setting)
        return setting

    async def update(self, setting: SiteSetting, updates: dict) -> SiteSetting:
        for key, value in updates.items():
            setattr(setting, key, value)
        await self.db.commit()
        await self.db.refresh(setting)
        return setting

    async def delete(self, setting: SiteSetting) -> None:
        await self.db.delete(setting)
        await self.db.commit()

