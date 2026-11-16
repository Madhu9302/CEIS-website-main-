from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.security import get_current_admin
from app.schemas.auth import LoginRequest, TokenResponse, UserResponse
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter(prefix="/admin/auth", tags=["Admin Portal - Auth"])

@router.post("/login", response_model=TokenResponse)
async def admin_login(
    payload: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    token_resp = await AuthService(db).authenticate_user(
        email=payload.email,
        password=payload.password,
        required_role="admin",
    )
    response.set_cookie(
        key="access_token",
        value=token_resp.access_token,
        httponly=True,
        samesite="lax",
    )
    return token_resp

@router.post("/logout")
async def admin_logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Admin logged out successfully"}

@router.get("/verify", response_model=UserResponse)
async def verify_admin_session(admin_user: User = Depends(get_current_admin)):
    return admin_user
