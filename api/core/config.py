# api/core/config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Informações do projeto
    PROJECT_NAME: str = "IA Open Source API"
    PROJECT_VERSION: str = "0.1.0"

    # CORS - origens permitidas (padrão localhost)
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    # Modo debug (True para desenvolvimento)
    DEBUG: bool = True

    # Prefixo opcional para rotas da API (ex: /api/v1)
    API_V1_STR: str = "/api/v1"

    # Configurações de serviços (ajustar conforme implantação)
    NLP_SERVICE_URL: str = "http://nlp_service:8001"
    LLM_SERVICE_URL: str = "http://llm_service:8002"
    VISION_SERVICE_URL: str = "http://vision_service:8003"
    SPEECH_SERVICE_URL: str = "http://speech_service:8004"
    SUMMARIZER_SERVICE_URL: str = "http://summarizer_service:8005"

    # Segurança
    SECRET_KEY: str = "change-me-in-production"
    API_KEY_HEADER: str = "X-API-Key"

    class Config:
        env_file = ".env"          # carrega variáveis do arquivo .env se existir
        case_sensitive = True

# Instância global para ser importada nos outros módulos
settings = Settings()
