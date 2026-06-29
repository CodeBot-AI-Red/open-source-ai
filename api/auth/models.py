# api/auth/models.py
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    READONLY = "readonly"


# ---------------------------------------------------------------------------
# JWT / Token
# ---------------------------------------------------------------------------
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Segundos até expirar o access token")


class TokenData(BaseModel):
    sub: str = Field(..., description="Identificador único do usuário (user_id ou e-mail)")
    role: UserRole = UserRole.USER
    jti: Optional[str] = None   # JWT ID — usado para blacklist de tokens revogados
    exp: Optional[datetime] = None


# ---------------------------------------------------------------------------
# Usuário
# ---------------------------------------------------------------------------
class UserBase(BaseModel):
    email: str
    name: Optional[str] = None
    role: UserRole = UserRole.USER
    is_active: bool = True


class UserInDB(UserBase):
    id: str
    hashed_password: str
    created_at: datetime


class UserPublic(UserBase):
    id: str
    created_at: datetime


# ---------------------------------------------------------------------------
# API Key
# ---------------------------------------------------------------------------
class APIKeyCreate(BaseModel):
    label: str = Field(..., max_length=80, description="Nome descritivo para esta chave")
    expires_days: Optional[int] = Field(None, ge=1, le=365)


class APIKeyResponse(BaseModel):
    key_id: str
    label: str
    key_preview: str = Field(..., description="Prefixo visível (ex: sk-abc...)")
    raw_key: Optional[str] = Field(None, description="Chave completa — exibida apenas na criação")
    created_at: datetime
    expires_at: Optional[datetime]
    is_active: bool
