import uuid
from pydantic import BaseModel, EmailStr, ConfigDict

class UserSignupRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    full_name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: uuid.UUID
    full_name: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
