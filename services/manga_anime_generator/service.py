"""Inference service wrapper for Manga and Anime Image Generation enterprise pipeline."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict

from services.manga_anime_generator.generator import (
    MangaAnimeGenerationParams,
    generate_manga_anime_image,
)
from services.manga_anime_generator.styles import STYLE_PRESETS, ASPECT_RATIO_DIMENSIONS


app = FastAPI(
    title="Manga & Anime Image Generation Service",
    version="3.0.0",
    description="Dedicated enterprise engine for manga and anime image synthesis.",
)


class GenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Descrição visual do personagem ou cena de manga/anime")
    negative_prompt: Optional[str] = Field(None, description="Elementos a evitar na geração")
    style_preset: str = Field("shonen", description="Preset de estilo (shonen, shojo, seinen, chibi, etc.)")
    aspect_ratio: str = Field("1:1", description="Proporção da imagem (1:1, 16:9, 9:16, 3:4, 4:3)")
    width: Optional[int] = Field(None, ge=256, le=3840, description="Largura customizada em pixels")
    height: Optional[int] = Field(None, ge=256, le=3840, description="Altura customizada em pixels")
    num_inference_steps: int = Field(30, ge=10, le=150, description="Número de passos de difusão")
    guidance_scale: float = Field(7.5, ge=1.0, le=30.0, description="Escala de orientação CFG")
    seed: Optional[int] = Field(None, ge=0, description="Semente para reprodutibilidade")
    sampler: str = Field("Euler_a", description="Algoritmo de amostragem")
    color_mode: str = Field("full_color", description="Modo de cor (full_color, black_and_white, grayscale)")
    screentone_density: str = Field("medium", description="Densidade de retícula de mangá (none, low, medium, high)")
    panel_layout: Optional[str] = Field(None, description="Layout de painel (single, 2_panels, 4_grid, splash_page)")
    upscale_factor: float = Field(1.0, ge=1.0, le=4.0, description="Fator de super-resolução/upscale")


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "manga-anime-image-generator",
        "version": "3.0.0",
        "available_presets": list(STYLE_PRESETS.keys()),
    }


@app.get("/styles")
async def list_styles():
    return {
        "styles": [
            {
                "name": preset.name,
                "display_name": preset.display_name,
                "description": preset.description,
                "default_color_mode": preset.default_color_mode,
                "recommended_guidance": preset.recommended_guidance,
                "recommended_steps": preset.recommended_steps,
            }
            for preset in STYLE_PRESETS.values()
        ],
        "aspect_ratios": list(ASPECT_RATIO_DIMENSIONS.keys()),
    }


@app.post("/generate")
async def generate_image_endpoint(body: GenerationRequest):
    try:
        params = MangaAnimeGenerationParams(
            prompt=body.prompt,
            negative_prompt=body.negative_prompt,
            style_preset=body.style_preset,
            aspect_ratio=body.aspect_ratio,
            width=body.width,
            height=body.height,
            num_inference_steps=body.num_inference_steps,
            guidance_scale=body.guidance_scale,
            seed=body.seed,
            sampler=body.sampler,
            color_mode=body.color_mode,
            screentone_density=body.screentone_density,
            panel_layout=body.panel_layout,
            upscale_factor=body.upscale_factor,
        )
        result = generate_manga_anime_image(params)
        return result.__dict__
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro na geração de arte manga/anime: {exc}")
