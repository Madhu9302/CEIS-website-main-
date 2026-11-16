import sys
from pathlib import Path

# Ensure CEIS_backend directory is in sys.path
_backend_dir = str(Path(__file__).resolve().parent.parent)
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.core.config import settings
from app.db.session import engine, AsyncSessionLocal
from app.db.base import Base

# Models for table metadata registration
from app.models.user import User
from app.models.submission import Submission
from app.models.notification import Notification
from app.models.service import Service
from app.core.security import hash_password

# Routers
from app.routes.public.auth import router as public_auth_router
from app.routes.admin.auth import router as admin_auth_router
from app.routes.public.inquiries import router as public_inquiries_router
from app.routes.admin.notifications import router as admin_notifications_router
from app.routes.public.services import router as public_services_router
from app.routes.admin.services import router as admin_services_router

logger = logging.getLogger("ceis.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Create tables automatically if DB is connected
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("[DB] All database tables verified and created successfully.")
    except Exception as exc:
        logger.warning(
            f"[DB Connection Warning] Could not connect to PostgreSQL on port 5432: {exc}. "
            "Please ensure your PostgreSQL server is started."
        )

    # 2. Seed default super_admin if not exists
    try:
        async with AsyncSessionLocal() as session:
            res = await session.execute(select(User).where(User.email == settings.ADMIN_EMAIL))
            if not res.scalar_one_or_none():
                admin = User(
                    email=settings.ADMIN_EMAIL,
                    full_name="Tanishq (Super Admin)",
                    password_hash=hash_password(settings.ADMIN_PASSWORD),
                    role="super_admin",
                )
                session.add(admin)
                await session.commit()
                logger.info(f"[DB Seed] Default super_admin created: {settings.ADMIN_EMAIL}")
    except Exception as exc:
        logger.warning(f"[DB Seed Warning] Super admin auto-seed skipped: {exc}")

    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers under /api/v1
app.include_router(public_auth_router, prefix=settings.API_V1_STR)
app.include_router(public_inquiries_router, prefix=settings.API_V1_STR)
app.include_router(public_services_router, prefix=settings.API_V1_STR)
app.include_router(admin_auth_router, prefix=settings.API_V1_STR)
app.include_router(admin_notifications_router, prefix=settings.API_V1_STR)
app.include_router(admin_services_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}