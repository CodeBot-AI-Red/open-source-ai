# api/auth/jwt_handler.py
"""
Utilitários para criação e validação de tokens JWT.

Dependências:
    pip install python-jose[cryptography]
"""
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, status

from api.auth.models import TokenData, UserRole
from api.core.config import settings

try:
    from jose import JWTError, jwt
except ImportError as e:
    raise ImportError(
        "Instale 'python-jose[cryptography]' para habilitar autenticação JWT: "
        "pip install python-jose[cryptography]"
    ) from e


# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------
def _now_utc() -> datetime:
    return datetime.now(tz=timezone.utc)


def _build_payload(
    subject: str,
    role: UserRole,
    expires_delta: timedelta,
    token_type: str,
) -> dict:
    return {
        "sub": subject,
        "role": role.value,
        "type": token_type,
        "jti": str(uuid.uuid4()),
        "iat": _now_utc(),
        "exp": _now_utc() + expires_delta,
    }


# ---------------------------------------------------------------------------
# Criação de tokens
# ---------------------------------------------------------------------------
def create_access_token(subject: str, role: UserRole = UserRole.USER) -> str:
    """Gera um access token com validade curta (ACCESS_TOKEN_EXPIRE_MINUTES)."""
    payload = _build_payload(
        subject=subject,
        role=role,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access",
    )
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(subject: str, role: UserRole = UserRole.USER) -> str:
    """Gera um refresh token com validade longa (REFRESH_TOKEN_EXPIRE_DAYS)."""
    payload = _build_payload(
        subject=subject,
        role=role,
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        token_type="refresh",
    )
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


# ---------------------------------------------------------------------------
# Decodificação / validação
# ---------------------------------------------------------------------------
def _decode(token: str, expected_type: Optional[str] = None) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    if expected_type and payload.get("type") != expected_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Tipo de token incorreto. Esperado: '{expected_type}'.",
        )
    return payload


def decode_access_token(token: str) -> TokenData:
    """Valida um access token e retorna os dados do usuário."""
    payload = _decode(token, expected_type="access")
    return TokenData(
        sub=payload["sub"],
        role=UserRole(payload.get("role", UserRole.USER)),
        jti=payload.get("jti"),
        exp=datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
    )


def decode_refresh_token(token: str) -> TokenData:
    """Valida um refresh token (usado no endpoint /auth/refresh)."""
    payload = _decode(token, expected_type="refresh")
    return TokenData(
        sub=payload["sub"],
        role=UserRole(payload.get("role", UserRole.USER)),
        jti=payload.get("jti"),
        exp=datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
    )
