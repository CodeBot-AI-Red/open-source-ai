# api/routes/text_generation.py
import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from api.core.config import settings
from api.core.dependencies import get_current_user, get_http_client
from api.schemas.requests import ChatRequest, CompletionRequest
from api.schemas.responses import ChatResponse, CompletionResponse

router = APIRouter()


def _service_error(exc: Exception, route: str) -> HTTPException:
    if isinstance(exc, httpx.TimeoutException):
        return HTTPException(status_code=504, detail=f"Serviço LLM não respondeu a tempo ({route}).")
    return HTTPException(status_code=502, detail=f"Erro ao comunicar com o serviço LLM ({route}): {exc}")


# ---------------------------------------------------------------------------
# POST /generation/chat
# ---------------------------------------------------------------------------
@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat com o LLM",
    description="Envia um histórico de mensagens e recebe a resposta do modelo de linguagem.",
)
async def chat(
    body: ChatRequest,
    user=Depends(get_current_user),
    client: httpx.AsyncClient = Depends(get_http_client),
):
    if body.stream:
        # Redireciona para o endpoint de streaming
        return await stream_chat(body, user)

    try:
        async with client:
            r = await client.post(
                f"{settings.LLM_SERVICE_URL}/chat",
                json=body.model_dump(),
            )
        r.raise_for_status()
        return r.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as exc:
        raise _service_error(exc, "chat")


# ---------------------------------------------------------------------------
# POST /generation/chat/stream  (Server-Sent Events)
# ---------------------------------------------------------------------------
@router.post(
    "/chat/stream",
    summary="Chat com streaming (SSE)",
    description=(
        "Envia um histórico de mensagens e recebe a resposta token a token "
        "via Server-Sent Events (text/event-stream)."
    ),
)
async def stream_chat(
    body: ChatRequest,
    user=Depends(get_current_user),
):
    async def _event_generator():
        async with httpx.AsyncClient(timeout=httpx.Timeout(read=settings.SERVICE_READ_TIMEOUT)) as client:
            try:
                async with client.stream(
                    "POST",
                    f"{settings.LLM_SERVICE_URL}/chat/stream",
                    json=body.model_dump(),
                ) as r:
                    r.raise_for_status()
                    async for chunk in r.aiter_text():
                        if chunk:
                            yield f"data: {chunk}\n\n"
            except Exception as exc:
                yield f"data: {{\"error\": \"{exc}\"}}\n\n"
            finally:
                yield "data: [DONE]\n\n"

    return StreamingResponse(_event_generator(), media_type="text/event-stream")


# ---------------------------------------------------------------------------
# POST /generation/complete
# ---------------------------------------------------------------------------
@router.post(
    "/complete",
    response_model=CompletionResponse,
    summary="Completação de texto",
    description="Recebe um prompt e retorna o texto gerado pelo modelo.",
)
async def complete(
    body: CompletionRequest,
    user=Depends(get_current_user),
    client: httpx.AsyncClient = Depends(get_http_client),
):
    try:
        async with client:
            r = await client.post(
                f"{settings.LLM_SERVICE_URL}/complete",
                json=body.model_dump(),
            )
        r.raise_for_status()
        return r.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as exc:
        raise _service_error(exc, "complete")
