# api/routes/speech_to_text.py
import httpx
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from typing import Optional

from api.core.config import settings
from api.core.dependencies import get_current_user, get_http_client
from api.schemas.responses import TranscribeResponse

router = APIRouter()

_ALLOWED_AUDIO_TYPES = {
    "audio/mpeg",       # .mp3
    "audio/wav",        # .wav
    "audio/x-wav",
    "audio/ogg",        # .ogg
    "audio/webm",       # .webm
    "audio/mp4",        # .m4a
    "audio/flac",       # .flac
}
_MAX_BYTES = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024


def _service_error(exc: Exception) -> HTTPException:
    if isinstance(exc, httpx.TimeoutException):
        return HTTPException(status_code=504, detail="Serviço Speech não respondeu a tempo.")
    return HTTPException(status_code=502, detail=f"Erro ao comunicar com o serviço Speech: {exc}")


# ---------------------------------------------------------------------------
# POST /speech/transcribe
# ---------------------------------------------------------------------------
@router.post(
    "/transcribe",
    response_model=TranscribeResponse,
    summary="Transcrição de áudio",
    description=(
        "Recebe um arquivo de áudio e retorna a transcrição em texto. "
        "Suporta MP3, WAV, OGG, WebM, M4A e FLAC. "
        "O parâmetro `language` é opcional — sem ele o idioma é auto-detectado."
    ),
)
async def transcribe_audio(
    file: UploadFile = File(..., description="Arquivo de áudio"),
    language: Optional[str] = Form(None, description="Código ISO 639-1 (ex: 'pt', 'en')"),
    return_timestamps: bool = Form(False),
    user=Depends(get_current_user),
    client: httpx.AsyncClient = Depends(get_http_client),
):
    if file.content_type not in _ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Tipo de áudio não suportado: {file.content_type}. Use: {_ALLOWED_AUDIO_TYPES}",
        )

    content = await file.read()
    if len(content) > _MAX_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"Arquivo muito grande. Máximo: {settings.MAX_UPLOAD_SIZE_MB} MB.",
        )

    form_data = {}
    if language:
        form_data["language"] = language
    form_data["return_timestamps"] = str(return_timestamps).lower()

    try:
        async with client:
            r = await client.post(
                f"{settings.SPEECH_SERVICE_URL}/transcribe",
                files={"file": (file.filename, content, file.content_type)},
                data=form_data,
            )
        r.raise_for_status()
        return r.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as exc:
        raise _service_error(exc)
