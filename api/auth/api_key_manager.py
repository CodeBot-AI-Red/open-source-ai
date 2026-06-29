# api/auth/api_key_manager.py
"""
Gerenciamento de API Keys.

Fluxo:
  1. generate_api_key()    → gera uma chave aleatória segura
  2. hash_api_key()        → cria o hash SHA-256 para armazenamento no BD
  3. verify_api_key_hash() → valida a chave recebida contra o hash armazenado

Em produção substitua `_FAKE_KEY_STORE` por consultas assíncronas ao banco de dados.
"""
import hashlib
import hmac
import secrets
from datetime import datetime, timezone
from typing import Optional

from api.auth.models import APIKeyCreate, APIKeyResponse

# ---------------------------------------------------------------------------
# Geração e hashing
# ---------------------------------------------------------------------------
_KEY_PREFIX = "sk-"
_KEY_BYTES = 32  # 256 bits de entropia


def generate_api_key() -> str:
    """Gera uma API Key segura com prefixo legível (ex: sk-a1b2c3...)."""
    return _KEY_PREFIX + secrets.token_urlsafe(_KEY_BYTES)


def hash_api_key(raw_key: str) -> str:
    """
    Retorna o SHA-256 hexadecimal da chave.
    Armazene apenas o hash — nunca a chave em texto claro.
    """
    return hashlib.sha256(raw_key.encode()).hexdigest()


def constant_time_compare(a: str, b: str) -> bool:
    """Comparação em tempo constante para evitar ataques de timing."""
    return hmac.compare_digest(a.encode(), b.encode())


# ---------------------------------------------------------------------------
# Store em memória (substitua por repositório de BD em produção)
# ---------------------------------------------------------------------------
# Estrutura: { key_id: { "hash": str, "label": str, "is_active": bool, ... } }
_FAKE_KEY_STORE: dict[str, dict] = {}


async def create_api_key(payload: APIKeyCreate) -> APIKeyResponse:
    """
    Cria e armazena uma nova API Key.
    Retorna o objeto com a chave em texto claro APENAS neste momento.
    """
    import uuid
    from datetime import timedelta

    raw_key = generate_api_key()
    key_id = str(uuid.uuid4())
    now = datetime.now(tz=timezone.utc)
    expires_at = now + timedelta(days=payload.expires_days) if payload.expires_days else None

    _FAKE_KEY_STORE[key_id] = {
        "hash": hash_api_key(raw_key),
        "label": payload.label,
        "is_active": True,
        "created_at": now,
        "expires_at": expires_at,
    }

    return APIKeyResponse(
        key_id=key_id,
        label=payload.label,
        key_preview=raw_key[:10] + "...",
        raw_key=raw_key,  # exibido uma única vez
        created_at=now,
        expires_at=expires_at,
        is_active=True,
    )


async def verify_api_key_hash(raw_key: str) -> bool:
    """
    Verifica se a chave fornecida corresponde a algum registro ativo no store.
    Em produção: SELECT FROM api_keys WHERE hash = ? AND is_active = TRUE
    """
    incoming_hash = hash_api_key(raw_key)
    for record in _FAKE_KEY_STORE.values():
        if not record["is_active"]:
            continue
        if record.get("expires_at") and record["expires_at"] < datetime.now(tz=timezone.utc):
            continue
        if constant_time_compare(record["hash"], incoming_hash):
            return True
    return False


async def revoke_api_key(key_id: str) -> bool:
    """Desativa uma API Key pelo seu ID."""
    if key_id in _FAKE_KEY_STORE:
        _FAKE_KEY_STORE[key_id]["is_active"] = False
        return True
    return False


async def list_api_keys() -> list[APIKeyResponse]:
    """Lista todas as chaves sem expor o hash nem a chave em texto claro."""
    results = []
    for key_id, record in _FAKE_KEY_STORE.items():
        results.append(
            APIKeyResponse(
                key_id=key_id,
                label=record["label"],
                key_preview="sk-***",
                raw_key=None,
                created_at=record["created_at"],
                expires_at=record.get("expires_at"),
                is_active=record["is_active"],
            )
        )
    return results
