# api/schemas/responses.py
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Genérico
# ---------------------------------------------------------------------------
class ErrorResponse(BaseModel):
    error: str
    detail: str
    request_id: Optional[str] = None


# ---------------------------------------------------------------------------
# Text Analysis
# ---------------------------------------------------------------------------
class SentimentResponse(BaseModel):
    label: Literal["positive", "negative", "neutral", "mixed"]
    score: float = Field(..., ge=0.0, le=1.0, description="Confiança do modelo (0–1)")
    scores_by_label: Dict[str, float] = Field(default_factory=dict)


class Entity(BaseModel):
    text: str
    label: str
    start: int
    end: int
    score: float


class NERResponse(BaseModel):
    entities: List[Entity]
    total: int


class ClassifyResponse(BaseModel):
    label: str
    score: float
    all_labels: List[Dict[str, Any]] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Text Generation
# ---------------------------------------------------------------------------
class ChatResponse(BaseModel):
    id: str
    model: str
    message: str
    finish_reason: Literal["stop", "length", "error"]
    usage: Dict[str, int] = Field(
        default_factory=dict,
        description="Ex: {'prompt_tokens': 20, 'completion_tokens': 80, 'total_tokens': 100}",
    )


class CompletionResponse(BaseModel):
    id: str
    text: str
    finish_reason: Literal["stop", "length", "error"]
    usage: Dict[str, int] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Image Analysis
# ---------------------------------------------------------------------------
class ClassificationResult(BaseModel):
    label: str
    score: float


class FaceDetection(BaseModel):
    count: int
    bounding_boxes: List[Dict[str, int]]  # [{"x": 0, "y": 0, "w": 100, "h": 120}]


class ImageAnalysisResponse(BaseModel):
    task: str
    result: Any  # ClassificationResult | FaceDetection | str


# ---------------------------------------------------------------------------
# Speech to Text
# ---------------------------------------------------------------------------
class WordTimestamp(BaseModel):
    word: str
    start: float
    end: float


class TranscribeResponse(BaseModel):
    text: str
    language: str
    duration_seconds: Optional[float] = None
    words: Optional[List[WordTimestamp]] = None


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------
class ServiceStatus(BaseModel):
    name: str
    url: str
    status: Literal["ok", "degraded", "unreachable"]
    latency_ms: Optional[float] = None


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"]
    version: str
    services: List[ServiceStatus]
