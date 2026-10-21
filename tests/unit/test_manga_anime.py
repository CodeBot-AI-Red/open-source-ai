import pytest
from services.manga_anime_generator.generator import (
    MangaAnimeGenerationParams,
    generate_manga_anime_image,
    validate_and_resolve_dimensions,
)
from services.manga_anime_generator.styles import STYLE_PRESETS, enrich_prompt


def test_style_presets_exist():
    assert "shonen" in STYLE_PRESETS
    assert "seinen" in STYLE_PRESETS
    assert "cyberpunk_anime" in STYLE_PRESETS
    assert len(STYLE_PRESETS) == 11


def test_enrich_prompt():
    pos, neg = enrich_prompt("Guerreiro lendario", style_preset="shonen", color_mode="full_color")
    assert "Guerreiro lendario" in pos
    assert "dynamic shonen anime style" in pos
    assert "worst quality" in neg


def test_validate_and_resolve_dimensions():
    w, h = validate_and_resolve_dimensions("16:9", None, None, upscale_factor=1.0)
    assert w == 1280
    assert h == 720

    w_up, h_up = validate_and_resolve_dimensions("1:1", None, None, upscale_factor=2.0)
    assert w_up == 2048
    assert h_up == 2048


def test_generate_manga_anime_image():
    params = MangaAnimeGenerationParams(
        prompt="Garota mágica com cetro brilhante",
        style_preset="shojo",
        aspect_ratio="3:4",
        seed=12345,
    )
    result = generate_manga_anime_image(params)

    assert result.id.startswith("manga-img-")
    assert result.status == "completed"
    assert result.seed == 12345
    assert result.width == 864
    assert result.height == 1152
    assert "data:image/svg+xml;base64," in result.image_url_or_base64
    assert "shojo" in result.style_preset


def test_generate_empty_prompt_raises():
    with pytest.raises(ValueError, match="não pode ser vazio"):
        generate_manga_anime_image(MangaAnimeGenerationParams(prompt="   "))
