import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.service import Service


class ServiceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, active_only: bool = False) -> list[Service]:
        stmt = select(Service).order_by(Service.display_order.asc(), Service.created_at.desc())
        if active_only:
            stmt = stmt.where(Service.is_active.is_(True))
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, service_id: uuid.UUID) -> Service | None:
        result = await self.db.execute(select(Service).where(Service.id == service_id))
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str, active_only: bool = True) -> Service | None:
        stmt = select(Service).where(Service.slug == slug)
        if active_only:
            stmt = stmt.where(Service.is_active.is_(True))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, service: Service) -> Service:
        self.db.add(service)
        await self.db.commit()
        await self.db.refresh(service)
        return service

    async def update(self, service: Service, updates: dict) -> Service:
        for key, value in updates.items():
            setattr(service, key, value)
        await self.db.commit()
        await self.db.refresh(service)
        return service

    async def delete(self, service: Service) -> None:
        await self.db.delete(service)
        await self.db.commit()