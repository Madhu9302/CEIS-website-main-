import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.models.cms_window import CMSWindow
from app.schemas.cms_window import CMSWindowCreate, CMSWindowUpdate, CMSWindowResponse
from app.core.security import get_current_admin

router = APIRouter(prefix="/windows", tags=["CMS Windows & Case Studies"])


@router.get("", response_model=list[CMSWindowResponse])
async def list_windows(
    all: bool = Query(False, description="Include unpublished windows if true"),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(CMSWindow).order_by(CMSWindow.updated_at.desc())
    if not all:
        stmt = stmt.where(CMSWindow.is_published.is_(True))
    res = await db.execute(stmt)
    return list(res.scalars().all())


@router.get("/{slug}", response_model=CMSWindowResponse)
async def get_window_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    stmt = select(CMSWindow).where(CMSWindow.slug == slug, CMSWindow.is_published.is_(True))
    res = await db.execute(stmt)
    window = res.scalar_one_or_none()
    if not window:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Window not found")
    return window


@router.post("", response_model=CMSWindowResponse, status_code=status.HTTP_201_CREATED)
async def create_window(
    payload: CMSWindowCreate,
    _: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    res = await db.execute(select(CMSWindow).where(CMSWindow.slug == payload.slug))
    if res.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Window slug already exists")
    
    if payload.slot_id:
        slot_res = await db.execute(select(CMSWindow).where(CMSWindow.slot_id == payload.slot_id))
        if slot_res.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Slot ID already in use")

    window = CMSWindow(**payload.model_dump())
    db.add(window)
    await db.commit()
    await db.refresh(window)
    return window


@router.put("/{id}", response_model=CMSWindowResponse)
async def update_window(
    id: uuid.UUID,
    payload: CMSWindowUpdate,
    _: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    res = await db.execute(select(CMSWindow).where(CMSWindow.id == id))
    window = res.scalar_one_or_none()
    if not window:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Window not found")

    updates = payload.model_dump(exclude_unset=True)
    if "slug" in updates and updates["slug"] != window.slug:
        existing = await db.execute(select(CMSWindow).where(CMSWindow.slug == updates["slug"]))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Window slug already exists")

    if "slot_id" in updates and updates["slot_id"] and updates["slot_id"] != window.slot_id:
        slot_existing = await db.execute(select(CMSWindow).where(CMSWindow.slot_id == updates["slot_id"]))
        if slot_existing.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Slot ID already in use")

    for k, v in updates.items():
        setattr(window, k, v)

    await db.commit()
    await db.refresh(window)
    return window


@router.delete("/{id}")
async def delete_window(
    id: uuid.UUID,
    _: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    res = await db.execute(select(CMSWindow).where(CMSWindow.id == id))
    window = res.scalar_one_or_none()
    if not window:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Window not found")

    await db.delete(window)
    await db.commit()
    return {"message": "Window deleted successfully"}
