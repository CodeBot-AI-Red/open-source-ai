"""Model architecture specifications and metadata loader for the Large-Scale AI Platform."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass(frozen=True)
class ServiceParameterSpecs:
    service_name: str
    model_name: str
    parameter_count_numeric: int
    parameter_count_formatted: str
    architecture: str
    precision: str
    context_window: int | None = None
    description: str = ""


@dataclass(frozen=True)
class LargeLanguageModelSpecs:
    name: str = "luzia-llm-70b-moe"
    total_parameters_numeric: int = 70_000_000_000
    total_parameters_formatted: str = "70.0B (70 bilhões)"
    active_parameters_per_token: str = "13.0B"
    architecture: str = "Mixture-of-Experts (MoE 8x13B) Transformer"
    layers: int = 80
    hidden_dimension: int = 8192
    attention_heads: int = 64
    kv_heads: int = 8
    context_window: int = 131072
    vocab_size: int = 128000
    precision_support: list[str] = field(default_factory=lambda: ["FP16", "BF16", "INT8", "INT4 (AWQ/GPTQ)"])


@dataclass(frozen=True)
class PlatformParametersSummary:
    total_platform_parameters_numeric: int = 103_500_000_000
    total_platform_parameters_formatted: str = "103.5B (103,5 Bilhões)"
    llm: LargeLanguageModelSpecs = field(default_factory=LargeLanguageModelSpecs)
    subservices: list[ServiceParameterSpecs] = field(default_factory=lambda: [
        ServiceParameterSpecs(
            service_name="Vision Service",
            model_name="vit-giant-22b-multimodal",
            parameter_count_numeric=22_000_000_000,
            parameter_count_formatted="22.0B (22 bilhões)",
            architecture="Vision Transformer (ViT-Giant)",
            precision="FP16 / INT8",
            description="Modelo de alta precisão para classificação de imagens, detecção de objetos e descrição visual."
        ),
        ServiceParameterSpecs(
            service_name="NLP Service",
            model_name="roberta-xxl-multilingual-8b",
            parameter_count_numeric=8_000_000_000,
            parameter_count_formatted="8.0B (8 bilhões)",
            architecture="Bidirectional Encoder (RoBERTa XXL)",
            precision="FP16 / INT8",
            description="Processamento de Linguagem Natural, análise de sentimento, NER e classificação zero-shot."
        ),
        ServiceParameterSpecs(
            service_name="Summarizer Service",
            model_name="moe-summarizer-2b",
            parameter_count_numeric=2_000_000_000,
            parameter_count_formatted="2.0B (2 bilhões)",
            architecture="Encoder-Decoder Summarizer MoE",
            precision="FP16",
            context_window=32768,
            description="Sumarização abstrativa e extrativa de textos extensos com fallback automático."
        ),
        ServiceParameterSpecs(
            service_name="Speech Service",
            model_name="whisper-large-v3-extended-1.5b",
            parameter_count_numeric=1_500_000_000,
            parameter_count_formatted="1.5B (1,5 bilhão)",
            architecture="Encoder-Decoder Audio Transformer",
            precision="FP16",
            description="Transcrição de áudio multi-formato, auto-detecção de idiomas e timestamps por palavra."
        )
    ])


@dataclass(frozen=True)
class ModelInfo:
    name: str = "luzia-llm-70b-moe"
    version: str = "2.5.0"
    loaded: bool = True
    backend: str = "large-scale-moe-engine"
    specs: PlatformParametersSummary = field(default_factory=PlatformParametersSummary)


def get_model_info() -> ModelInfo:
    return ModelInfo()
