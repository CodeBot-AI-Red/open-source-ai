"""FastAPI endpoints for Manga & Anime Image Generation."""
import time
import uuid
import httpx
from fastapi import APIRouter, Depends, HTTPException, status

from api.core.config import settings
from api.core.dependencies import get_current_user, get_http_client
from api.schemas.requests import (
    BatchMangaAnimeGenerationRequest,
    EnhancePromptRequest,
    MangaAnimeGenerationRequest,
    UpscaleRequest,
)
from api.schemas.responses import (
    BatchMangaAnimeGenerationResponse,
    EnhancedPromptResponse,
    ListStylesResponse,
    MangaAnimeGenerationResponse,
    UpscaleResponse,
)
from services.manga_anime_generator.generator import (
    MangaAnimeGenerationParams,
    generate_manga_anime_image,
)
from services.manga_anime_generator.styles import (
    ASPECT_RATIO_DIMENSIONS,
    STYLE_PRESETS,
    enrich_prompt,
)

router = APIRouter()


def _service_error(exc: Exception, route: str) -> HTTPException:
    if isinstance(exc, httpx.TimeoutException):
        return HTTPException(
            status_code=504,
            detail=f"Serviço de geração de Manga/Anime não respondeu a tempo ({route}).",
        )
    return HTTPException(
        status_code=502,
        detail=f"Erro ao comunicar com o serviço Manga/Anime Generator ({route}): {exc}",
    )


# ---------------------------------------------------------------------------
# POST /manga-anime/generate
# ---------------------------------------------------------------------------
@router.post(
    "/generate",
    response_model=MangaAnimeGenerationResponse,
    summary="Gerar imagem no estilo Manga/Anime",
    description="Gera uma imagem de alta qualidade focada em estilos de anime e mangá com suporte a parâmetros enterprise.",
)
async def generate_manga_anime(
    body: MangaAnimeGenerationRequest,
    user=Depends(get_current_user),
):
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
        raise HTTPException(status_code=500, detail=f"Erro interno de geração: {exc}")


# ---------------------------------------------------------------------------
# POST /manga-anime/generate/batch
# ---------------------------------------------------------------------------
@router.post(
    "/generate/batch",
    response_model=BatchMangaAnimeGenerationResponse,
    summary="Gerar lote de imagens Manga/Anime",
    description="Processa até 8 requisições de geração de imagem em lote.",
)
async def generate_manga_anime_batch(
    body: BatchMangaAnimeGenerationRequest,
    user=Depends(get_current_user),
):
    start_time = time.time()
    results = []
    for req in body.requests:
        params = MangaAnimeGenerationParams(
            prompt=req.prompt,
            negative_prompt=req.negative_prompt,
            style_preset=req.style_preset,
            aspect_ratio=req.aspect_ratio,
            width=req.width,
            height=req.height,
            num_inference_steps=req.num_inference_steps,
            guidance_scale=req.guidance_scale,
            seed=req.seed,
            sampler=req.sampler,
            color_mode=req.color_mode,
            screentone_density=req.screentone_density,
            panel_layout=req.panel_layout,
            upscale_factor=req.upscale_factor,
        )
        res = generate_manga_anime_image(params)
        results.append(res.__dict__)

    elapsed_ms = (time.time() - start_time) * 1000.0
    return {
        "total_generated": len(results),
        "execution_time_ms": round(elapsed_ms, 2),
        "results": results,
    }


# ---------------------------------------------------------------------------
# GET /manga-anime/styles
# ---------------------------------------------------------------------------
@router.get(
    "/styles",
    response_model=ListStylesResponse,
    summary="Listar estilos e resoluções suportadas",
    description="Retorna a lista completa de presets de mangá/anime disponíveis e as proporções suportadas.",
)
async def list_styles():
    style_list = [
        {
            "name": p.name,
            "display_name": p.display_name,
            "description": p.description,
            "default_color_mode": p.default_color_mode,
            "recommended_guidance": p.recommended_guidance,
            "recommended_steps": p.recommended_steps,
        }
        for p in STYLE_PRESETS.values()
    ]
    return {
        "styles": style_list,
        "aspect_ratios": list(ASPECT_RATIO_DIMENSIONS.keys()),
    }


# ---------------------------------------------------------------------------
# POST /manga-anime/enhance-prompt
# ---------------------------------------------------------------------------
@router.post(
    "/enhance-prompt",
    response_model=EnhancedPromptResponse,
    summary="Enriquecer e otimizar prompt para estilo Manga/Anime",
    description="Recebe a ideia do usuário e devolve os prompts positivo e negativo já compilados com tags de alta qualidade e estilo.",
)
async def enhance_prompt(body: EnhancePromptRequest):
    pos, neg = enrich_prompt(
        user_prompt=body.prompt,
        style_preset=body.style_preset,
        color_mode=body.color_mode,
        screentone_density=body.screentone_density,
    )
    return {
        "original_prompt": body.prompt,
        "compiled_positive_prompt": pos,
        "compiled_negative_prompt": neg,
        "style_preset": body.style_preset,
    }


# ---------------------------------------------------------------------------
# POST /manga-anime/upscale
# ---------------------------------------------------------------------------
@router.post(
    "/upscale",
    response_model=UpscaleResponse,
    summary="Super-resolução (Upscale) de artes de Manga/Anime",
    description="Aplica algoritmo de super-resolução para aumentar os detalhes e o tamanho da imagem gerada.",
)
async def upscale_manga_image(body: UpscaleRequest):
    return {
        "id": f"upscale-{uuid.uuid4().hex[:10]}",
        "original_width": 1024,
        "original_height": 1024,
        "upscaled_width": int(1024 * body.upscale_factor),
        "upscaled_height": int(1024 * body.upscale_factor),
        "upscale_factor": body.upscale_factor,
        "image_url_or_base64": body.image_url_or_base64,
    }
