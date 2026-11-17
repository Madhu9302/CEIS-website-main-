from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.security import get_current_admin
from app.schemas.auth import LoginRequest, UserResponse
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["CEIS-D1 Contract - Auth"])


class VaultUserSummary(BaseModel):
    email: EmailStr
    role: str
    full_name: str | None = None


class VaultTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user: VaultUserSummary


@router.post("/login", response_model=VaultTokenResponse)
async def vault_login(
    payload: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    token_resp = await AuthService(db).authenticate_user(
        email=str(payload.email),
        password=payload.password,
        required_role="admin",
    )
    response.set_cookie(
        key="access_token",
        value=token_resp.access_token,
        httponly=True,
        samesite="lax",
    )
    return VaultTokenResponse(
        access_token=token_resp.access_token,
        token_type="bearer",
        role=token_resp.role,
        user=VaultUserSummary(
            email=payload.email,
            role=token_resp.role,
        ),
    )


@router.get("/me", response_model=UserResponse)
async def get_current_vault_user(admin_user: User = Depends(get_current_admin)):
    return admin_user