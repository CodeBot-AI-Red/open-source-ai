# api/routes/image_analysis.py
import httpx
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from api.core.config import settings
from api.core.dependencies import get_current_user, get_http_client
from api.schemas.requests import ImageURLRequest
from api.schemas.responses import ImageAnalysisResponse

router = APIRouter()

_ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
_MAX_BYTES = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024


def _service_error(exc: Exception, route: str) -> HTTPException:
    if isinstance(exc, httpx.TimeoutException):
        return HTTPException(status_code=504, detail=f"Serviço Vision não respondeu a tempo ({route}).")
    return HTTPException(status_code=502, detail=f"Erro ao comunicar com o serviço Vision ({route}): {exc}")


# ---------------------------------------------------------------------------
# POST /vision/upload
# ---------------------------------------------------------------------------
@router.post(
    "/upload",
    response_model=ImageAnalysisResponse,
    summary="Analisar imagem (upload)",
    description="Envia uma imagem por multipart/form-data para classificação, detecção de faces ou descrição.",
)
async def analyze_image_upload(
    file: UploadFile = File(..., description="Arquivo de imagem (JPEG, PNG, WebP, GIF)"),
    task: str = Query("classify", enum=["classify", "detect_faces", "describe"]),
    user=Depends(get_current_user),
    client: httpx.AsyncClient = Depends(get_http_client),
):
    if file.content_type not in _ALLOWED_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Tipo de arquivo não suportado: {file.content_type}. Use: {_ALLOWED_TYPES}",
        )

    content = await file.read()
    if len(content) > _MAX_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"Arquivo muito grande. Máximo: {settings.MAX_UPLOAD_SIZE_MB} MB.",
        )

    try:
        async with client:
            r = await client.post(
                f"{settings.VISION_SERVICE_URL}/{task}",
                files={"file": (file.filename, content, file.content_type)},
            )
        r.raise_for_status()
        return ImageAnalysisResponse(task=task, result=r.json())
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as exc:
        raise _service_error(exc, task)


# ---------------------------------------------------------------------------
# POST /vision/url
# ---------------------------------------------------------------------------
@router.post(
    "/url",
    response_model=ImageAnalysisResponse,
    summary="Analisar imagem (URL)",
    description="Envia a URL de uma imagem pública para análise pelo serviço de visão.",
)
async def analyze_image_url(
    body: ImageURLRequest,
    user=Depends(get_current_user),
    client: httpx.AsyncClient = Depends(get_http_client),
):
    try:
        async with client:
            r = await client.post(
                f"{settings.VISION_SERVICE_URL}/{body.task}",
                json={"url": body.url},
            )
        r.raise_for_status()
        return ImageAnalysisResponse(task=body.task, result=r.json())
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as exc:
        raise _service_error(exc, body.task)
