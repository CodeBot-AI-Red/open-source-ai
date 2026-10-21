# api/main.py
import logging
from contextlib import asynccontextmanager

import httpx
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api.core.config import settings
from starlette.middleware.cors import CORSMiddleware

from api.middleware.cors import cors_kwargs
from api.middleware.logging import LoggingMiddleware
from api.middleware.rate_limit import RateLimitMiddleware
from api.middleware.request_id import RequestIDMiddleware
from api.routes import (
    health,
    manga_anime,
)
from api.auth.jwt_handler import decode_access_token
from api.auth.api_key_manager import verify_api_key_hash

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Lifespan: startup / shutdown
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Iniciando Manga & Anime Image Generation API v%s", settings.PROJECT_VERSION)

    services = {
        "manga_anime_generator": settings.MANGA_ANIME_SERVICE_URL,
    }

    async with httpx.AsyncClient(timeout=5.0) as client:
        for name, url in services.items():
            try:
                r = await client.get(f"{url}/health")
                if r.status_code == 200:
                    logger.info("  ✅ Serviço '%s' acessível em %s", name, url)
                else:
                    logger.warning("  ⚠️  Serviço '%s' retornou status %s", name, r.status_code)
            except Exception as e:
                logger.warning("  ⚠️  Serviço '%s' não está acessível em %s: %s", name, url, str(e))

    logger.info("📦 IA Especializada em Mangá e Anime pronta para receber requisições.")
    yield

    logger.info("🛑 Encerrando Manga & Anime API — recursos liberados.")


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=(
        "API Enterprise dedicada exclusivamente à geração de imagens, ilustrações, "
        "personagens e páginas no estilo Mangá e Anime com parametrização avançada "
        "(Shonen, Shojo, Seinen, Chibi, Cyberpunk, 90s Retro, Retículas, Samplers e Upscaling)."
    ),
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# Middlewares
# ---------------------------------------------------------------------------
app.add_middleware(RequestIDMiddleware)
app.add_middleware(CORSMiddleware, **cors_kwargs())
app.add_middleware(RateLimitMiddleware)
app.add_middleware(LoggingMiddleware)


# ---------------------------------------------------------------------------
# Dependência de autenticação global
# ---------------------------------------------------------------------------
async def auth_dependency(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cabeçalho Authorization ausente",
        )

    # Tenta JWT
    if auth_header.startswith("Bearer "):
        token = auth_header[len("Bearer ") :]
        decode_access_token(token)
        return True

    # Tenta API Key (formato: "ApiKey <key>")
    if auth_header.startswith("ApiKey "):
        api_key = auth_header[len("ApiKey ") :]
        if await verify_api_key_hash(api_key):
            return True
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API Key inválida",
            )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Formato de autenticação não suportado",
    )


# ---------------------------------------------------------------------------
# Exception handlers globais
# ---------------------------------------------------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "validation_error",
            "detail": exc.errors(),
            "request_id": getattr(request.state, "request_id", None),
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "request_id": getattr(request.state, "request_id", None),
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Erro não tratado na rota %s", request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "internal_server_error",
            "detail": "Ocorreu um erro interno. Tente novamente mais tarde.",
            "request_id": getattr(request.state, "request_id", None),
        },
    )


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
v1 = settings.API_V1_STR

# Rotas públicas
app.include_router(health.router, prefix=v1, tags=["Health"])

# Rotas protegidas (Manga & Anime Generator)
app.include_router(
    manga_anime.router,
    prefix=f"{v1}/manga-anime",
    tags=["Manga & Anime Generation"],
    dependencies=[Depends(auth_dependency)],
)


# ---------------------------------------------------------------------------
# Rota raiz
# ---------------------------------------------------------------------------
@app.get("/", tags=["Root"])
async def root():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "docs": f"{settings.API_V1_STR}/docs",
    }
