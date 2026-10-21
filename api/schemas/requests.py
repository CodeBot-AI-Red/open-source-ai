from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Manga & Anime Image Generation Schemas
# ---------------------------------------------------------------------------

StylePresetType = Literal[
    "shonen",
    "shojo",
    "seinen",
    "chibi",
    "classic_90s",
    "cyberpunk_anime",
    "ink_manga_bw",
    "webtoon_color",
    "cel_shaded",
    "dark_fantasy_manga",
    "mecha",
]

AspectRatioType = Literal["1:1", "16:9", "9:16", "3:4", "4:3"]
ColorModeType = Literal["full_color", "black_and_white", "grayscale"]
ScreentoneDensityType = Literal["none", "low", "medium", "high"]
PanelLayoutType = Literal["single", "2_panels", "4_grid", "splash_page"]


class MangaAnimeGenerationRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="Prompt em texto descrevendo a cena, personagem ou ambiente de manga/anime.",
        json_schema_extra={"example": "Guerreiro jovem com espada de energia em uma cidade cyberpunk ao pôr do sol"},
    )
    negative_prompt: Optional[str] = Field(
        None,
        max_length=2000,
        description="Prompt negativo customizado para remover características indesejadas.",
        json_schema_extra={"example": "desfocado, proporção incorreta, braços extras"},
    )
    style_preset: StylePresetType = Field(
        "shonen",
        description="Estilo pré-definido de arte de anime ou manga.",
    )
    aspect_ratio: AspectRatioType = Field(
        "1:1",
        description="Proporção da imagem gerada.",
    )
    width: Optional[int] = Field(
        None,
        ge=256,
        le=3840,
        description="Largura personalizada em pixels (deve ser múltiplo de 8 se fornecido).",
    )
    height: Optional[int] = Field(
        None,
        ge=256,
        le=3840,
        description="Altura personalizada em pixels (deve ser múltiplo de 8 se fornecido).",
    )
    num_inference_steps: int = Field(
        30,
        ge=10,
        le=150,
        description="Número de passos de inferência/difusão.",
    )
    guidance_scale: float = Field(
        7.5,
        ge=1.0,
        le=30.0,
        description="Fator de fidelidade ao prompt (CFG Scale).",
    )
    seed: Optional[int] = Field(
        None,
        ge=0,
        description="Semente aleatória para geração determinística.",
    )
    sampler: str = Field(
        "Euler_a",
        description="Algoritmo de amostragem de difusão (Euler_a, DPM++_2M_Karras, DDIM, UniPC).",
    )
    color_mode: ColorModeType = Field(
        "full_color",
        description="Modo de renderização de cor (full_color, black_and_white, grayscale).",
    )
    screentone_density: ScreentoneDensityType = Field(
        "medium",
        description="Densidade de pontos de retícula de mangá (screentone) para estilos P&B.",
    )
    panel_layout: Optional[PanelLayoutType] = Field(
        None,
        description="Estrutura de diagramação de painel de mangá.",
    )
    upscale_factor: float = Field(
        1.0,
        ge=1.0,
        le=4.0,
        description="Fator de super-resolução/upscale pós-geração (1.0, 1.5, 2.0, 4.0).",
    )


class BatchMangaAnimeGenerationRequest(BaseModel):
    requests: List[MangaAnimeGenerationRequest] = Field(
        ...,
        min_length=1,
        max_length=8,
        description="Lista de requisições de geração em lote para alta vazão.",
    )


class EnhancePromptRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000)
    style_preset: StylePresetType = "shonen"
    color_mode: ColorModeType = "full_color"
    screentone_density: ScreentoneDensityType = "medium"


class UpscaleRequest(BaseModel):
    image_url_or_base64: str = Field(..., description="URL ou string Base64 da imagem para upscale")
    upscale_factor: float = Field(2.0, ge=1.5, le=4.0, description="Fator de super-resolução")
