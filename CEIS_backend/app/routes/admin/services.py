import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.service_repo import ServiceRepository
from app.services.service_cms_service import ServiceCMSService
from app.schemas.service import ServiceCreate, ServiceUpdate, ServiceResponse
from app.core.permissions import get_current_admin
from app.models.user import User

router = APIRouter(prefix="/admin/services", tags=["Admin CMS - Services"])


def get_cms_service(db: AsyncSession = Depends(get_db)) -> ServiceCMSService:
    return ServiceCMSService(ServiceRepository(db))


@router.get("", response_model=list[ServiceResponse])
async def admin_list_services(
    _: User = Depends(get_current_admin),
    service: ServiceCMSService = Depends(get_cms_service),
):
    return await service.list_all_services()


@router.post("", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
async def admin_create_service(
    payload: ServiceCreate,
    _: User = Depends(get_current_admin),
    service: ServiceCMSService = Depends(get_cms_service),
):
    return await service.create_service(payload)


@router.patch("/{service_id}", response_model=ServiceResponse)
async def admin_update_service(
    service_id: uuid.UUID,
    payload: ServiceUpdate,
    _: User = Depends(get_current_admin),
    service: ServiceCMSService = Depends(get_cms_service),
):
    return await service.update_service(service_id, payload)


@router.delete("/{service_id}")
async def admin_delete_service(
    service_id: uuid.UUID,
    _: User = Depends(get_current_admin),
    service: ServiceCMSService = Depends(get_cms_service),
):
    return await service.delete_service(service_id)