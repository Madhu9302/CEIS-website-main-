from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.service_repo import ServiceRepository
from app.services.service_cms_service import ServiceCMSService
from app.schemas.service import ServiceResponse

router = APIRouter(prefix="/public/services", tags=["Public CMS - Services"])


def get_cms_service(db: AsyncSession = Depends(get_db)) -> ServiceCMSService:
    return ServiceCMSService(ServiceRepository(db))


@router.get("", response_model=list[ServiceResponse])
async def list_services(service: ServiceCMSService = Depends(get_cms_service)):
    return await service.list_public_services()


@router.get("/{slug}", response_model=ServiceResponse)
async def get_service_detail(slug: str, service: ServiceCMSService = Depends(get_cms_service)):
    return await service.get_public_service_by_slug(slug)