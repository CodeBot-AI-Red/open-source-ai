import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.auth.jwt_handler import create_access_token

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Manga & Anime" in data["service"]


def test_list_styles_unauthenticated_fails():
    response = client.get("/api/v1/manga-anime/styles")
    assert response.status_code == 401


def test_list_styles_authenticated():
    token = create_access_token(subject="user123")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/manga-anime/styles", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["styles"]) == 11
    assert "16:9" in data["aspect_ratios"]


def test_generate_image_authenticated():
    token = create_access_token(subject="user123")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "prompt": "Robô mecha gigante em combate em Neo-Tokyo",
        "style_preset": "mecha",
        "aspect_ratio": "16:9",
        "color_mode": "full_color",
        "num_inference_steps": 35,
        "seed": 42,
    }
    response = client.post("/api/v1/manga-anime/generate", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["style_preset"] == "mecha"
    assert data["width"] == 1280
    assert data["height"] == 720
    assert data["seed"] == 42


def test_enhance_prompt():
    token = create_access_token(subject="user123")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "prompt": "Samurai de katana sob a lua cheia",
        "style_preset": "seinen",
        "color_mode": "black_and_white",
    }
    response = client.post("/api/v1/manga-anime/enhance-prompt", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "seinen" in data["style_preset"]
    assert "intricate seinen manga" in data["compiled_positive_prompt"]
