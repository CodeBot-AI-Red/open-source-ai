"""Definitions and preset configurations for Manga & Anime Image Generation.

Provides style profiles, quality prompts, negative prompts, aspect ratio maps,
and prompt enrichment capabilities for high-throughput enterprise generation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class StylePreset:
    name: str
    display_name: str
    description: str
    positive_suffix: str
    negative_suffix: str
    default_color_mode: str = "full_color"
    recommended_guidance: float = 7.5
    recommended_steps: int = 30


STYLE_PRESETS: Dict[str, StylePreset] = {
    "shonen": StylePreset(
        name="shonen",
        display_name="Shonen Action",
        description="Dynamic action lines, expressive characters, vivid contrast, energetic anime composition.",
        positive_suffix="dynamic shonen anime style, energetic action pose, bold lineart, cinematic anime lighting, masterpiece, high quality anime key visual",
        negative_suffix="dull, flat colors, blurry lineart, distorted anatomy, low quality, watermark",
        default_color_mode="full_color",
        recommended_guidance=7.5,
        recommended_steps=30,
    ),
    "shojo": StylePreset(
        name="shojo",
        display_name="Shojo Romance",
        description="Delicate fine lines, soft pastel tones, emotional expressive eyes, floral and romantic accents.",
        positive_suffix="delicate shojo manga visual style, soft ethereal lighting, expressive sparkling eyes, aesthetic pastel palette, fine detailed lineart",
        negative_suffix="harsh dark shadows, coarse lines, grotesque, realistic photo, blurry, bad anatomy",
        default_color_mode="full_color",
        recommended_guidance=7.0,
        recommended_steps=28,
    ),
    "seinen": StylePreset(
        name="seinen",
        display_name="Seinen / Mature Manga",
        description="Intricate dark ink hatching, mature proportions, dramatic contrast, high-detail graphic novel aesthetic.",
        positive_suffix="intricate seinen manga art style, detailed black ink cross-hatching, realistic anime proportions, dramatic shadow contrast, masterpiece",
        negative_suffix="oversaturated cartoon, chibi proportions, blurry, low resolution, extra limbs",
        default_color_mode="black_and_white",
        recommended_guidance=8.0,
        recommended_steps=35,
    ),
    "chibi": StylePreset(
        name="chibi",
        display_name="Chibi / Super Deformed",
        description="Super deformed cute proportions, big emotive eyes, rounded clean outlines, bright cheerful colors.",
        positive_suffix="cute chibi anime style, super deformed 2 head tall proportions, big cute shiny eyes, clean thick outlines, adorable pastel aesthetic",
        negative_suffix="tall realistic proportions, gory, hyperrealistic face, sharp dark shadows, ugly",
        default_color_mode="full_color",
        recommended_guidance=7.0,
        recommended_steps=25,
    ),
    "classic_90s": StylePreset(
        name="classic_90s",
        display_name="90s Retro Anime",
        description="Hand-drawn 90s aesthetic, classic cel shading, subtle film grain, vintage anime OVA vibe.",
        positive_suffix="1990s retro anime aesthetic, hand-drawn cel animation style, subtle film grain aesthetic, classic 90s anime visual, masterpiece",
        negative_suffix="modern 3D CGI, digital gradient overkill, ultra glossy render, blur, bad anatomy",
        default_color_mode="full_color",
        recommended_guidance=7.5,
        recommended_steps=32,
    ),
    "cyberpunk_anime": StylePreset(
        name="cyberpunk_anime",
        display_name="Cyberpunk Anime",
        description="Futuristic neon cityscapes, holographic glints, detailed tech gear, sci-fi anime vibe.",
        positive_suffix="futuristic cyberpunk anime art, glowing neon reflections, detailed tech implants and mechanical gear, cinematic sci-fi anime atmosphere",
        negative_suffix="fantasy medieval, dull colors, low contrast, washed out, blurry",
        default_color_mode="full_color",
        recommended_guidance=8.0,
        recommended_steps=35,
    ),
    "ink_manga_bw": StylePreset(
        name="ink_manga_bw",
        display_name="Traditional Black & White Manga",
        description="Authentic Japanese manga page rendering with screen tones, pen ink hatching and speech panel harmony.",
        positive_suffix="traditional Japanese manga page, authentic black and white G-pen ink, screentone shading dots, clean manga panel aesthetic, high contrast manga drawing",
        negative_suffix="color, pastel, gradient, 3D render, photo, color bleed, low resolution",
        default_color_mode="black_and_white",
        recommended_guidance=8.5,
        recommended_steps=35,
    ),
    "webtoon_color": StylePreset(
        name="webtoon_color",
        display_name="Modern Color Webtoon",
        description="Vibrant digital full-color webcomic style, smooth lighting gradients, crisp digital line art.",
        positive_suffix="modern full-color Korean webtoon art style, smooth digital shading, vibrant colors, clean vector-like lineart, glossy anime finish",
        negative_suffix="greyscale, rough pencil, noisy texture, 3D polygon, blurry, bad hand",
        default_color_mode="full_color",
        recommended_guidance=7.0,
        recommended_steps=28,
    ),
    "cel_shaded": StylePreset(
        name="cel_shaded",
        display_name="Modern Cel-Shaded Key Art",
        description="Clean anime key art rendering, sharp shadows, vivid studio anime production polish.",
        positive_suffix="modern anime studio key art, sharp cel shading boundaries, clean outlines, vibrant studio animation quality, highly detailed",
        negative_suffix="soft blurry brushwork, realistic oil painting, noise, pixelated, bad anatomy",
        default_color_mode="full_color",
        recommended_guidance=7.5,
        recommended_steps=30,
    ),
    "dark_fantasy_manga": StylePreset(
        name="dark_fantasy_manga",
        display_name="Dark Fantasy Manga",
        description="Atmospheric darkness, ominous mist, highly detailed armor and weaponry, dark manga art.",
        positive_suffix="dark fantasy manga aesthetic, intense dramatic chiaroscuro lighting, highly detailed dark armor and blade, mysterious atmospheric fog",
        negative_suffix="bright rainbow colors, cheerful cute aesthetic, low resolution, bad hands, distorted anatomy",
        default_color_mode="black_and_white",
        recommended_guidance=8.5,
        recommended_steps=38,
    ),
    "mecha": StylePreset(
        name="mecha",
        display_name="Mecha & Sci-Fi Anime",
        description="Precision mechanical armor, metallic highlights, optical lenses, intricate panel seams.",
        positive_suffix="intricate sci-fi mecha anime style, detailed robot armor panels, glowing optical sensors, metallic surface highlights, anime mecha art",
        negative_suffix="organic blob, low detail, soft fluffy textures, blurry, malformed hydraulics",
        default_color_mode="full_color",
        recommended_guidance=8.0,
        recommended_steps=35,
    ),
}

DEFAULT_QUALITY_TAGS = "best quality, masterwork, highly detailed manga/anime artwork"
DEFAULT_NEGATIVE_PROMPT = "worst quality, low quality, bad anatomy, deformed limbs, extra fingers, missing fingers, blurry, watermark, signature, distorted face, bad proportions"

ASPECT_RATIO_DIMENSIONS: Dict[str, Tuple[int, int]] = {
    "1:1": (1024, 1024),
    "16:9": (1280, 720),
    "9:16": (720, 1280),
    "3:4": (864, 1152),
    "4:3": (1152, 864),
}


def enrich_prompt(
    user_prompt: str,
    style_preset: str = "shonen",
    color_mode: str = "full_color",
    screentone_density: str = "medium",
    add_quality_tags: bool = True,
) -> Tuple[str, str]:
    """Compiles and enriches user prompt and negative prompt with style-specific tags."""
    preset = STYLE_PRESETS.get(style_preset, STYLE_PRESETS["shonen"])

    prompt_parts: List[str] = [user_prompt.strip()]

    if add_quality_tags:
        prompt_parts.append(DEFAULT_QUALITY_TAGS)

    if preset.positive_suffix:
        prompt_parts.append(preset.positive_suffix)

    if color_mode in ("black_and_white", "grayscale"):
        tone_str = f"{screentone_density} density manga screentones" if screentone_density != "none" else "monochrome ink"
        prompt_parts.append(f"monochrome, black and white manga ink, {tone_str}")

    compiled_positive = ", ".join(prompt_parts)

    negative_parts: List[str] = [DEFAULT_NEGATIVE_PROMPT]
    if preset.negative_suffix:
        negative_parts.append(preset.negative_suffix)

    if color_mode in ("black_and_white", "grayscale"):
        negative_parts.append("color, colorful, vibrant chromatic colors, color tint")

    compiled_negative = ", ".join(negative_parts)

    return compiled_positive, compiled_negative
