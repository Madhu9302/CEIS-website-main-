import uuid
from fastapi import HTTPException, status
from app.models.service import Service
from app.repositories.service_repo import ServiceRepository
from app.schemas.service import ServiceCreate, ServiceUpdate


class ServiceCMSService:
    def __init__(self, repo: ServiceRepository):
        self.repo = repo

    async def list_public_services(self) -> list[Service]:
        return await self.repo.get_all(active_only=True)

    async def get_public_service_by_slug(self, slug: str) -> Service:
        service = await self.repo.get_by_slug(slug, active_only=True)
        if not service:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
        return service

    async def list_all_services(self) -> list[Service]:
        return await self.repo.get_all(active_only=False)

    async def create_service(self, payload: ServiceCreate) -> Service:
        existing = await self.repo.get_by_slug(payload.slug, active_only=False)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Service slug already exists")
        service = Service(**payload.model_dump())
        return await self.repo.create(service)

    async def update_service(self, service_id: uuid.UUID, payload: ServiceUpdate) -> Service:
        service = await self.repo.get_by_id(service_id)
        if not service:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
        updates = payload.model_dump(exclude_unset=True)
        if "slug" in updates and updates["slug"] != service.slug:
            existing = await self.repo.get_by_slug(updates["slug"], active_only=False)
            if existing:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Service slug already exists")
        return await self.repo.update(service, updates)

    async def delete_service(self, service_id: uuid.UUID) -> dict:
        service = await self.repo.get_by_id(service_id)
        if not service:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
        await self.repo.delete(service)
        return {"message": "Service deleted successfully"}