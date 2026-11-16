from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.security import get_current_user
from app.schemas.auth import UserSignupRequest, UserResponse, TokenResponse
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter(prefix="/public/auth", tags=["Public Portal - Auth"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def public_signup(
    payload: UserSignupRequest,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    user = await AuthService(db).register_public_user(payload)
    return user

@router.post("/login", response_model=TokenResponse)
async def public_login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    token_resp = await AuthService(db).authenticate_user(
        email=form_data.username,
        password=form_data.password
    )
    # Set HttpOnly cookie for web security
    response.set_cookie(
        key="access_token",
        value=token_resp.access_token,
        httponly=True,
        samesite="lax",
    )
    return token_resp

@router.post("/logout")
async def public_logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
async def get_public_profile(current_user: User = Depends(get_current_user)):
    return current_user
