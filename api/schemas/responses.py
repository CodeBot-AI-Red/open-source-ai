from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Generico
# ---------------------------------------------------------------------------
class ErrorResponse(BaseModel):
    error: str
    detail: str
    request_id: Optional[str] = None


# ---------------------------------------------------------------------------
# Manga & Anime Image Generation Schemas
# ---------------------------------------------------------------------------
class MangaAnimeGenerationResponse(BaseModel):
    id: str = Field(..., description="ID único da geração da imagem")
    created_at: float = Field(..., description="Timestamp UNIX de criação")
    status: Literal["completed", "failed"] = Field("completed", description="Status do job de geração")
    prompt_used: str = Field(..., description="Prompt final enriquecido utilizado pelo motor")
    negative_prompt_used: str = Field(..., description="Prompt negativo final compilado")
    style_preset: str = Field(..., description="Preset de estilo aplicado")
    width: int = Field(..., description="Largura final da imagem em pixels")
    height: int = Field(..., description="Altura final da imagem em pixels")
    num_inference_steps: int = Field(..., description="Passos de difusão executados")
    guidance_scale: float = Field(..., description="Escala de orientação CFG utilizada")
    seed: int = Field(..., description="Semente aleatória utilizada")
    sampler: str = Field(..., description="Sampler de amostragem utilizado")
    color_mode: str = Field(..., description="Modo de cor (full_color, black_and_white, grayscale)")
    panel_layout: Optional[str] = Field(None, description="Layout do painel de mangá")
    upscale_factor: float = Field(..., description="Fator de super-resolução aplicado")
    execution_time_ms: float = Field(..., description="Tempo total de processamento em milissegundos")
    image_url_or_base64: str = Field(..., description="URL ou payload Base64/Data-URI da imagem gerada")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadados adicionais do motor")


class BatchMangaAnimeGenerationResponse(BaseModel):
    total_generated: int
    execution_time_ms: float
    results: List[MangaAnimeGenerationResponse]


class StyleInfo(BaseModel):
    name: str
    display_name: str
    description: str
    default_color_mode: str
    recommended_guidance: float
    recommended_steps: int


class ListStylesResponse(BaseModel):
    styles: List[StyleInfo]
    aspect_ratios: List[str]


class EnhancedPromptResponse(BaseModel):
    original_prompt: str
    compiled_positive_prompt: str
    compiled_negative_prompt: str
    style_preset: str


class UpscaleResponse(BaseModel):
    id: str
    original_width: int
    original_height: int
    upscaled_width: int
    upscaled_height: int
    upscale_factor: float
    image_url_or_base64: str


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
