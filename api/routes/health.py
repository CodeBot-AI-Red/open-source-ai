# api/routes/health.py
import asyncio
import time
from datetime import datetime, timezone

import httpx
from fastapi import APIRouter

from api.core.config import settings
from api.schemas.responses import HealthResponse, ServiceStatus

router = APIRouter()

_SERVICES = {
    "nlp": settings.NLP_SERVICE_URL,
    "llm": settings.LLM_SERVICE_URL,
    "vision": settings.VISION_SERVICE_URL,
    "speech": settings.SPEECH_SERVICE_URL,
    "summarizer": settings.SUMMARIZER_SERVICE_URL,
}


async def _probe(client: httpx.AsyncClient, name: str, url: str) -> ServiceStatus:
    start = time.perf_counter()
    try:
        r = await client.get(f"{url}/health", timeout=3.0)
        latency = (time.perf_counter() - start) * 1000
        status = "ok" if r.status_code == 200 else "degraded"
    except Exception:
        latency = None
        status = "unreachable"

    return ServiceStatus(name=name, url=url, status=status, latency_ms=latency)


@router.get("/health", summary="Liveness probe")
async def health_check():
    """Verifica se a API está no ar (Kubernetes liveness probe)."""
    return {
        "status": "ok",
        "version": settings.PROJECT_VERSION,
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }


@router.get("/ready", summary="Readiness probe")
async def readiness_check():
    """
    Verifica se a API e todos os serviços dependentes estão prontos
    (Kubernetes readiness probe). Retorna 503 se algum serviço crítico
    estiver inacessível.
    """
    async with httpx.AsyncClient() as client:
        probes = await asyncio.gather(
            *[_probe(client, name, url) for name, url in _SERVICES.items()]
        )

    overall = "ok" if all(s.status == "ok" for s in probes) else "degraded"

    return HealthResponse(
        status=overall,
        version=settings.PROJECT_VERSION,
        services=list(probes),
    )
