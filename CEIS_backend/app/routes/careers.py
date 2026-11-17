from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.models.career import CareerRole
from app.schemas.career import CareerRoleCreate, CareerRoleResponse
from app.core.security import get_current_admin

router = APIRouter(prefix="/careers", tags=["Careers & Roles"])


@router.get("", response_model=list[CareerRoleResponse])
async def list_careers(db: AsyncSession = Depends(get_db)):
    stmt = select(CareerRole).where(CareerRole.is_active.is_(True)).order_by(CareerRole.created_at.desc())
    res = await db.execute(stmt)
    return list(res.scalars().all())


@router.post("", response_model=CareerRoleResponse, status_code=status.HTTP_201_CREATED)
async def create_career_role(
    payload: CareerRoleCreate,
    _: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    role = CareerRole(**payload.model_dump())
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role
