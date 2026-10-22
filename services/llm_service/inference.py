"""FastAPI entrypoint for the local LLM service."""
from __future__ import annotations

import json
import hashlib
import math
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from services.llm_service.chat_handler import GenerationConfig, PromptSafetyError, chat, trim_to_token_budget
from services.llm_service.model_loader import get_model_info


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str = Field(..., min_length=1)


class ChatRequest(BaseModel):
    messages: list[Message] = Field(..., min_length=1)
    max_tokens: int = Field(512, ge=1, le=4096)
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    top_p: float = Field(1.0, ge=0.0, le=1.0)
    presence_penalty: float = Field(0.0, ge=-2.0, le=2.0)
    frequency_penalty: float = Field(0.0, ge=-2.0, le=2.0)
    stream: bool = False


class CompletionRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=8000)
    max_tokens: int = Field(256, ge=1, le=4096)
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    top_p: float = Field(1.0, ge=0.0, le=1.0)
    presence_penalty: float = Field(0.0, ge=-2.0, le=2.0)
    frequency_penalty: float = Field(0.0, ge=-2.0, le=2.0)


class EmbeddingRequest(BaseModel):
    input: str | list[str] = Field(..., description="Texto ou lista de textos para gerar embeddings.")
    model: str = Field("luzia-embed-large-v1", description="Nome do modelo de embedding")
    dimensions: int = Field(1536, ge=128, le=4096)


app = FastAPI(title="Open Source AI LLM Service", version="2.5.0")


def _generate_embedding_vector(text: str, dim: int = 1536) -> list[float]:
    """Gera um vetor denso normalizado determinístico de dimensão N baseado no hash do texto."""
    seed = hashlib.sha256(text.encode("utf-8")).digest()
    raw_vector = []
    for i in range(dim):
        b = seed[i % len(seed)]
        val = math.sin((i + 1) * b)
        raw_vector.append(val)
    norm = math.sqrt(sum(v * v for v in raw_vector)) or 1.0
    return [round(v / norm, 6) for v in raw_vector]


@app.get("/health")
async def health() -> dict[str, str]:
    info = get_model_info()
    return {"status": "ok", "model": info.name, "parameters": info.specs.total_platform_parameters_formatted}


@app.get("/models")
async def models_endpoint():
    info = get_model_info()
    return {
        "model": info.name,
        "version": info.version,
        "backend": info.backend,
        "total_platform_parameters": info.specs.total_platform_parameters_formatted,
        "total_platform_parameters_numeric": info.specs.total_platform_parameters_numeric,
        "llm_specs": {
            "name": info.specs.llm.name,
            "total_parameters": info.specs.llm.total_parameters_formatted,
            "total_parameters_numeric": info.specs.llm.total_parameters_numeric,
            "active_parameters_per_token": info.specs.llm.active_parameters_per_token,
            "architecture": info.specs.llm.architecture,
            "layers": info.specs.llm.layers,
            "hidden_dimension": info.specs.llm.hidden_dimension,
            "attention_heads": info.specs.llm.attention_heads,
            "kv_heads": info.specs.llm.kv_heads,
            "context_window": info.specs.llm.context_window,
            "precision_support": info.specs.llm.precision_support,
        },
        "subservices_specs": [
            {
                "service": spec.service_name,
                "model": spec.model_name,
                "parameters": spec.parameter_count_formatted,
                "parameters_numeric": spec.parameter_count_numeric,
                "architecture": spec.architecture,
                "precision": spec.precision,
                "description": spec.description,
            }
            for spec in info.specs.subservices
        ],
    }


@app.post("/chat")
async def chat_endpoint(body: ChatRequest):
    try:
        config = GenerationConfig(
            max_tokens=body.max_tokens,
            temperature=body.temperature,
            top_p=body.top_p,
            presence_penalty=body.presence_penalty,
            frequency_penalty=body.frequency_penalty,
        )
        result = chat([m.model_dump() for m in body.messages], config)
    except PromptSafetyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return result.__dict__


@app.post("/complete")
async def complete_endpoint(body: CompletionRequest):
    config = GenerationConfig(
        max_tokens=body.max_tokens,
        temperature=body.temperature,
        top_p=body.top_p,
        presence_penalty=body.presence_penalty,
        frequency_penalty=body.frequency_penalty,
    )
    result = chat([{"role": "user", "content": body.prompt}], config)
    text, reason = trim_to_token_budget(result.message, body.max_tokens)
    return {"id": result.id.replace("chatcmpl", "cmpl"), "text": text, "finish_reason": reason, "usage": result.usage}


@app.post("/chat/stream")
async def stream_chat_endpoint(body: ChatRequest):
    async def events():
        config = GenerationConfig(
            max_tokens=body.max_tokens,
            temperature=body.temperature,
            top_p=body.top_p,
            presence_penalty=body.presence_penalty,
            frequency_penalty=body.frequency_penalty,
        )
        result = chat([m.model_dump() for m in body.messages], config)
        for token in result.message.split():
            yield json.dumps({"token": token + " "}, ensure_ascii=False) + "\n"
        yield json.dumps({"finish_reason": result.finish_reason, "usage": result.usage}, ensure_ascii=False) + "\n"

    return StreamingResponse(events(), media_type="application/x-ndjson")


@app.post("/embeddings")
async def embeddings_endpoint(body: EmbeddingRequest):
    inputs = [body.input] if isinstance(body.input, str) else body.input
    data = []
    total_tokens = 0
    for idx, text in enumerate(inputs):
        vec = _generate_embedding_vector(text, dim=body.dimensions)
        tokens = max(1, len(text.split()))
        total_tokens += tokens
        data.append({
            "object": "embedding",
            "index": idx,
            "embedding": vec,
        })
    return {
        "object": "list",
        "data": data,
        "model": body.model,
        "usage": {
            "prompt_tokens": total_tokens,
            "total_tokens": total_tokens,
        },
    }
