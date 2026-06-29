# api/routes/text_analysis.py
import httpx
from fastapi import APIRouter, Depends, HTTPException, status

from api.core.config import settings
from api.core.dependencies import get_current_user, get_http_client
from api.schemas.requests import NERRequest, SentimentRequest, TextClassifyRequest
from api.schemas.responses import ClassifyResponse, NERResponse, SentimentResponse

router = APIRouter()


def _service_error(exc: Exception, route: str) -> HTTPException:
    if isinstance(exc, httpx.TimeoutException):
        return HTTPException(status_code=504, detail=f"Serviço NLP não respondeu a tempo ({route}).")
    return HTTPException(status_code=502, detail=f"Erro ao comunicar com o serviço NLP ({route}): {exc}")


# ---------------------------------------------------------------------------
# POST /analysis/sentiment
# ---------------------------------------------------------------------------
@router.post(
    "/sentiment",
    response_model=SentimentResponse,
    summary="Análise de sentimento",
    description="Classifica o sentimento de um texto em positivo, negativo, neutro ou misto.",
)
async def analyze_sentiment(
    body: SentimentRequest,
    user=Depends(get_current_user),
    client: httpx.AsyncClient = Depends(get_http_client),
):
    try:
        async with client:
            r = await client.post(
                f"{settings.NLP_SERVICE_URL}/sentiment",
                json=body.model_dump(),
            )
        r.raise_for_status()
        return r.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as exc:
        raise _service_error(exc, "sentiment")


# ---------------------------------------------------------------------------
# POST /analysis/ner
# ---------------------------------------------------------------------------
@router.post(
    "/ner",
    response_model=NERResponse,
    summary="Reconhecimento de entidades (NER)",
    description="Extrai entidades nomeadas (pessoas, organizações, locais…) do texto.",
)
async def extract_entities(
    body: NERRequest,
    user=Depends(get_current_user),
    client: httpx.AsyncClient = Depends(get_http_client),
):
    try:
        async with client:
            r = await client.post(
                f"{settings.NLP_SERVICE_URL}/ner",
                json=body.model_dump(),
            )
        r.raise_for_status()
        return r.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as exc:
        raise _service_error(exc, "ner")


# ---------------------------------------------------------------------------
# POST /analysis/classify
# ---------------------------------------------------------------------------
@router.post(
    "/classify",
    response_model=ClassifyResponse,
    summary="Classificação de texto",
    description=(
        "Classifica o texto em categorias. Se `labels` for informado, "
        "executa classificação zero-shot; caso contrário usa o modelo padrão."
    ),
)
async def classify_text(
    body: TextClassifyRequest,
    user=Depends(get_current_user),
    client: httpx.AsyncClient = Depends(get_http_client),
):
    try:
        async with client:
            r = await client.post(
                f"{settings.NLP_SERVICE_URL}/classify",
                json=body.model_dump(),
            )
        r.raise_for_status()
        return r.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as exc:
        raise _service_error(exc, "classify")
