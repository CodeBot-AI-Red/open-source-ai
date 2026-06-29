# api/schemas/requests.py
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Text Analysis (NLP)
# ---------------------------------------------------------------------------
class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Texto para análise de sentimento")
    language: str = Field("pt", description="Código ISO 639-1 do idioma")

    model_config = {"json_schema_extra": {"example": {"text": "Adorei o produto, excelente qualidade!", "language": "pt"}}}


class NERRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    entities: List[str] = Field(
        default=["PER", "ORG", "LOC", "MISC"],
        description="Tipos de entidade a extrair",
    )


class TextClassifyRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    labels: Optional[List[str]] = Field(None, description="Rótulos candidatos (zero-shot). Se None, usa o modelo padrão.")


# ---------------------------------------------------------------------------
# Text Generation (LLM)
# ---------------------------------------------------------------------------
class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str = Field(..., min_length=1)


class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(..., min_items=1)
    max_tokens: int = Field(512, ge=1, le=4096)
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    stream: bool = False

    model_config = {
        "json_schema_extra": {
            "example": {
                "messages": [{"role": "user", "content": "Explique machine learning em 3 frases."}],
                "max_tokens": 256,
                "temperature": 0.7,
                "stream": False,
            }
        }
    }


class CompletionRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=8000)
    max_tokens: int = Field(256, ge=1, le=4096)
    temperature: float = Field(0.7, ge=0.0, le=2.0)


# ---------------------------------------------------------------------------
# Image Analysis (Vision)
# ---------------------------------------------------------------------------
class ImageURLRequest(BaseModel):
    url: str = Field(..., description="URL pública da imagem")
    task: Literal["classify", "detect_faces", "describe"] = "classify"


# ---------------------------------------------------------------------------
# Speech to Text
# ---------------------------------------------------------------------------
class TranscribeRequest(BaseModel):
    language: Optional[str] = Field(None, description="Idioma esperado (ex: 'pt', 'en'). Se None, auto-detecta.")
    return_timestamps: bool = Field(False, description="Inclui timestamps por palavra na resposta")
