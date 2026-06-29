# api/core/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from api.core.config import settings

# ------------------------------------------------------------
# 1. Autenticação via API Key (simples, para testes iniciais)
# ------------------------------------------------------------
api_key_header = APIKeyHeader(name=settings.API_KEY_HEADER, auto_error=False)

async def verify_api_key(api_key: str = Depends(api_key_header)):
    """
    Valida a chave de API recebida no header X-API-Key.
    Em produção, substituir pela consulta ao banco de chaves (api_key_manager).
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key ausente. Inclua o header X-API-Key.",
        )
    # Placeholder: compara com uma chave mestra definida nas settings
    # Na versão final, use o api_key_manager para verificar hashes no banco.
    if api_key != settings.SECRET_KEY:  # Apenas para desenvolvimento!
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key inválida.",
        )
    return api_key

# ------------------------------------------------------------
# 2. Autenticação via JWT (Bearer Token)
# ------------------------------------------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Extrai e valida um token JWT do header Authorization: Bearer <token>.
    Retorna o payload decodificado (dados do usuário).
    Em produção, a lógica de decodificação será movida para auth/jwt_handler.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de acesso ausente.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # Tentativa de usar python-jose (instale com: pip install python-jose[cryptography])
        from jose import JWTError, jwt

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload  # payload contém 'sub', 'exp', etc.
    except ImportError:
        # Fallback simples: apenas verifica se o token é a própria SECRET_KEY (desenvolvimento)
        if token != settings.SECRET_KEY:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token inválido. Instale 'python-jose' para validação JWT completa.",
            )
        # Retorna um payload fictício
        return {"sub": "dev-user", "role": "admin"}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token inválido ou expirado.",
        )
