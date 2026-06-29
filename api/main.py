# api/main.py
import logging
import uuid
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.core.config import settings
from api.middleware.logging import LoggingMiddleware
from api.middleware.rate_limit import RateLimitMiddleware
from api.routes import health, image_analysis, speech_to_text, text_analysis, text_generation

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
    logger.info("🚀 Iniciando IA Open Source API v%s", settings.PROJECT_VERSION)

    # Verifica conectividade com os serviços internos de forma não-bloqueante
    services = {
        "nlp": settings.NLP_SERVICE_URL,
        "llm": settings.LLM_SERVICE_URL,
        "vision": settings.VISION_SERVICE_URL,
        "speech": settings.SPEECH_SERVICE_URL,
        "summarizer": settings.SUMMARIZER_SERVICE_URL,
    }
    async with httpx.AsyncClient(timeout=3.0) as client:
        for name, url in services.items():
            try:
                r = await client.get(f"{url}/health")
                if r.status_code == 200:
                    logger.info("  ✅ Serviço '%s' acessível em %s", name, url)
                else:
                    logger.warning("  ⚠️  Serviço '%s' retornou status %s", name, r.status_code)
            except Exception:
                logger.warning("  ⚠️  Serviço '%s' não está acessível em %s", name, url)

    yield

    logger.info("🛑 Encerrando IA Open Source API — recursos liberados.")


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=(
        "API central do IA Open Source. Oferece endpoints unificados para "
        "análise de texto, geração de texto (LLM), visão computacional e "
        "transcrição de áudio, com autenticação JWT/API-Key e rate limiting."
    ),
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# Middlewares (ordem importa: último adicionado = primeiro executado)
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(LoggingMiddleware)


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
            "request_id": request.state.request_id if hasattr(request.state, "request_id") else None,
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

app.include_router(health.router, prefix=v1, tags=["Health"])
app.include_router(text_analysis.router, prefix=f"{v1}/analysis", tags=["Text Analysis"])
app.include_router(text_generation.router, prefix=f"{v1}/generation", tags=["Text Generation"])
app.include_router(image_analysis.router, prefix=f"{v1}/vision", tags=["Image Analysis"])
app.include_router(speech_to_text.router, prefix=f"{v1}/speech", tags=["Speech to Text"])


# ---------------------------------------------------------------------------
# Rota raiz
# ---------------------------------------------------------------------------
@app.get("/", tags=["Root"])
async def root():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "docs": f"{v1}/docs",
    }
