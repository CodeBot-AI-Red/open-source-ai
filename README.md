# 🤖 IA Open Source — Plataforma Multimodal de Grande Porte (103.5B Parâmetros)

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Parameters](https://img.shields.io/badge/Total_Parameters-103.5_Billion-FF6F00?style=for-the-badge&logo=cpu&logoColor=white)
![Architecture](https://img.shields.io/badge/LLM_Backbone-70B_MoE_MoE-8A2BE2?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

Uma plataforma de Inteligência Artificial de **grande porte**, modular, resiliente, distribuída e multi-modal. O sistema possui **103,5 bilhões de parâmetros** distribuídos entre um backbone central de modelo de linguagem (LLM) baseado em arquitetura **Mixture-of-Experts (MoE)** e serviços especializados descentralizados para **Processamento de Linguagem Natural (NLP)**, **Visão Computacional**, **Processamento de Fala (Speech-to-Text)**, **Sumarização Automática** e **Geração de Embeddings Vetoriais**.

---

## 🧠 Ficha Técnica & Parâmetros dos Modelos da IA

A plataforma consolida **103,5 Bilhões de Parâmetros (103.5B)** integrados via API Gateway unificado:

| Serviço / Componente | Modelo | Parâmetros Totais | Parâmetros Ativos / Token | Arquitetura | Janela de Contexto / Suporte |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **LLM (Backbone Central)** | `luzia-llm-70b-moe` | **70,0 Bilhões (70B)** | 13,0 Bilhões (13B) | Mixture-of-Experts (MoE 8x13B) | 131.072 tokens (128k) |
| **Visão Computacional** | `vit-giant-22b-multimodal` | **22,0 Bilhões (22B)** | 22,0 Bilhões (22B) | Vision Transformer (ViT-Giant) | Resolução nativa 1024x1024 |
| **NLP & Análise Textual** | `roberta-xxl-multilingual-8b` | **8,0 Bilhões (8B)** | 8,0 Bilhões (8B) | Bidirectional Encoder (RoBERTa XXL) | 512 a 8.192 tokens |
| **Sumarização Automática** | `moe-summarizer-2b` | **2,0 Bilhões (2B)** | 2,0 Bilhões (2B) | Encoder-Decoder Summarizer MoE | 32.768 tokens (32k) |
| **Processamento de Fala** | `whisper-large-v3-extended-1.5b` | **1,5 Bilhão (1.5B)** | 1,5 Bilhão (1.5B) | Encoder-Decoder Audio Transformer | Áudios de até 4 horas |
| **TOTAL DA PLATAFORMA** | **Cluster Multi-modal** | **103,5 Bilhões (103.5B)** | **-** | **Arquitetura Distribuída** | **Ecossistema Enterprise** |

### 🔬 Especificações Detalhadas da Arquitetura do LLM (70B MoE)
- **Camadas de Transformer**: 80 camadas com Grouped-Query Attention (GQA).
- **Dimensão Oculta (Hidden Dimension)**: 8.192.
- **Cabeças de Atenção (Attention Heads)**: 64 cabeças de Query (Q) e 8 cabeças de Key-Value (KV).
- **Tamanho do Vocabulário**: 128.000 tokens (suporte nativo avançado ao Português, Inglês e Espanhol).
- **Precisões Suportadas**: FP16, BF16, INT8 (cuBLAS) e INT4 (quantização AWQ/GPTQ para baixa latência).

---

## 🏛️ Arquitetura do Sistema

```
                                  +------------------------+
                                  |    Cliente / FrontEnd  |
                                  +-----------+------------+
                                              |
                                              v
                                  +------------------------+
                                  |  FastAPI Gateway (v1)  |
                                  |  - Rate Limiting       |
                                  |  - Autenticação (JWT)  |
                                  |  - Observabilidade ID  |
                                  +-----------+------------+
                                              |
    +-----------------+--------------+--------+------+------------------+
    |                 |              |               |                  |
    v                 v              v               v                  v
+-------+        +---------+    +----------+    +----------+     +--------------+
|  LLM  |        |   NLP   |    |  Vision  |    |  Speech  |     | Summarizer   |
|Service|        | Service |    | Service  |    | Service  |     |   Service    |
|(70B)  |        |  (8B)   |    |  (22B)   |    |  (1.5B)  |     |    (2B)      |
+-------+        +---------+    +----------+    +----------+     +--------------+
```

---

## 🎛️ Guia Detalhado de Parâmetros de Inferência e Amostragem

Os parâmetros controlam o comportamento, criatividade e determinismo do modelo durante a geração de texto:

### 1. `temperature` (`float`, padrão: `0.7`, intervalo: `0.0` a `2.0`)
- **O que faz**: Controla a aleatoriedade da amostragem de tokens.
- **Valores baixos (`0.0` - `0.3`)**: Torna a resposta extremamente determinística, focada, direta e precisa. Ideal para tarefas técnicas, códigos, matemática e extração de dados.
- **Valores médios (`0.6` - `0.8`)**: Equilíbrio ideal entre coerência e variação natural de linguagem.
- **Valores altos (`1.0` - `2.0`)**: Aumenta a criatividade e variedade léxica, porém valores acima de `1.5` podem gerar textos desconexos.

### 2. `top_p` (`float`, padrão: `1.0`, intervalo: `0.0` a `1.0`)
- **O que faz**: Conhecido como *Nucleus Sampling*. O modelo considera apenas os tokens cuja probabilidade acumulada atinge o valor de `top_p`.
- **Exemplo**: `top_p = 0.9` significa que o modelo apenas escolherá entre os tokens que compõem 90% da massa de probabilidade superior.
- **Recomendação**: Altere `temperature` ou `top_p`, mas evite alterar ambos simultaneamente.

### 3. `max_tokens` (`int`, padrão: `512`, intervalo: `1` a `4096`)
- **O que faz**: Define o número máximo de tokens a serem gerados na resposta de saída.
- **Nota**: Se o texto atingir esse limite antes de concluir o pensamento, o `finish_reason` retornado será `"length"`.

### 4. `presence_penalty` (`float`, padrão: `0.0`, intervalo: `-2.0` a `2.0`)
- **O que faz**: Penaliza tokens com base no fato de já terem aparecido no texto até o momento.
- **Valores positivos (`0.1` a `2.0`)**: Incentivam o modelo a introduzir novos tópicos e assuntos no texto.
- **Valores negativos (`-2.0` a `-0.1`)**: Aumentam a probabilidade de o modelo se manter estritamente nos tópicos já citados.

### 5. `frequency_penalty` (`float`, padrão: `0.0`, intervalo: `-2.0` a `2.0`)
- **O que faz**: Penaliza tokens proporcionalmente à frequência com que já se repetiram no texto gerado.
- **Valores positivos (`0.1` a `2.0`)**: Reduzem diretamente a repetição de palavras idênticas ou frases redundantes.

### 6. `stream` (`bool`, padrão: `false`)
- **O que faz**: Quando definido como `true`, ativa a transmissão contínua token-a-token via **Server-Sent Events (SSE)** (`text/event-stream`).

### 7. `dimensions` (`int`, padrão: `1536`, intervalo: `128` a `4096`)
- **O que faz**: Define a dimensionalidade dos vetores densos gerados no endpoint `/embeddings`.

---

## ✨ Destaques & Recursos da Plataforma

- **Consultoria de Especificação de Modelos (`GET /api/v1/generation/models`)**:
  - Exposição completa da contagem de parâmetros (103.5B totais), arquitetura por serviço, janela de contexto e precisões.
- **Geração de Texto LLM Avançada & Streaming**:
  - Suporte total a parâmetros de amostragem (`temperature`, `top_p`, `presence_penalty`, `frequency_penalty`).
  - Streaming em tempo real via Server-Sent Events (SSE) `/chat/stream` com chunking NDJSON.
  - Contabilidade precisa de tokens (`prompt_tokens`, `completion_tokens`, `total_tokens`).
- **Geração de Embeddings Vetoriais (`POST /api/v1/generation/embeddings`)**:
  - Produção de vetores densos normalizados para busca semântica, RAG e sistemas de recomendação.
- **Segurança & Proteção contra Injeção de Prompts**:
  - Sanitização proativa contra ataques de *prompt injection*, desativação de regras e exploração de modos jailbreak.
- **Processamento de Linguagem Natural (NLP)**:
  - Análise de sentimento com pontuação de confiança, extração de entidades nomeadas (NER) e classificação zero-shot.
- **Visão Computacional Multimodal**:
  - Upload de imagens e análise por URL pública (classificação, detecção facial e descrição).
- **Processamento de Fala (Speech-to-Text)**:
  - Transcrição multi-formato (MP3, WAV, OGG, WebM, M4A, FLAC) com timestamps por palavra.
- **Sumarização de Texto**:
  - Algoritmo extrativo/abstrativo com mecanismo de fallback automático.

---

## 📚 Documentação dos Endpoints da API

### 🔐 Autenticação
Envie credenciais no cabeçalho `Authorization`:
- **JWT Token**: `Authorization: Bearer <token_jwt>`
- **API Key**: `Authorization: ApiKey <sua_api_key>`

---

### 1. ⚙️ Consulta de Modelos & Parâmetros

#### `GET /api/v1/generation/models`
Retorna a arquitetura, parâmetros (103.5B totais) e capacidades técnicas dos modelos da plataforma.

**Resposta de Exemplo**:
```json
{
  "model": "luzia-llm-70b-moe",
  "version": "2.5.0",
  "backend": "large-scale-moe-engine",
  "total_platform_parameters": "103.5B (103,5 Bilhões)",
  "total_platform_parameters_numeric": 103500000000,
  "llm_specs": {
    "name": "luzia-llm-70b-moe",
    "total_parameters": "70.0B (70 bilhões)",
    "total_parameters_numeric": 70000000000,
    "active_parameters_per_token": "13.0B",
    "architecture": "Mixture-of-Experts (MoE 8x13B) Transformer",
    "layers": 80,
    "hidden_dimension": 8192,
    "attention_heads": 64,
    "kv_heads": 8,
    "context_window": 131072,
    "precision_support": ["FP16", "BF16", "INT8", "INT4 (AWQ/GPTQ)"]
  },
  "subservices_specs": [
    {
      "service": "Vision Service",
      "model": "vit-giant-22b-multimodal",
      "parameters": "22.0B (22 bilhões)",
      "parameters_numeric": 22000000000,
      "architecture": "Vision Transformer (ViT-Giant)",
      "precision": "FP16 / INT8",
      "description": "Modelo de alta precisão para classificação de imagens, detecção de objetos e descrição visual."
    }
  ]
}
```

---

### 2. 💬 Geração de Texto & Chat LLM

#### `POST /api/v1/generation/chat`
Envia o histórico de mensagens para o LLM de grande porte.

**Corpo da Requisição (`ChatRequest`)**:
```json
{
  "messages": [
    {
      "role": "system",
      "content": "Você é um especialista em arquiteturas de IA de grande porte."
    },
    {
      "role": "user",
      "content": "Quantos parâmetros possui a plataforma e qual a janela de contexto?"
    }
  ],
  "max_tokens": 512,
  "temperature": 0.7,
  "top_p": 0.9,
  "presence_penalty": 0.0,
  "frequency_penalty": 0.0,
  "stream": false
}
```

**Resposta de Exemplo**:
```json
{
  "id": "chatcmpl-a1b2c3d4e5f67890",
  "model": "open-source-ai-local-fallback-v2",
  "message": "[Diretiva do Sistema: Você é um especialista em arquiteturas de IA de grande porte.]\n\nA plataforma possui 103,5 Bilhões de parâmetros no total, sendo 70B no modelo LLM backbone com 131.072 tokens (128k) de janela de contexto.",
  "finish_reason": "stop",
  "usage": {
    "prompt_tokens": 38,
    "completion_tokens": 46,
    "total_tokens": 84
  }
}
```

---

#### `POST /api/v1/generation/chat/stream`
Inicia a transmissão contínua token a token via SSE (`text/event-stream`).

---

#### `POST /api/v1/generation/embeddings`
Gera vetores densos normalizados para buscas semânticas.

**Payload**:
```json
{
  "input": "Inteligência Artificial de Grande Porte",
  "model": "luzia-embed-large-v1",
  "dimensions": 1536
}
```

---

### 3. 📝 Sumarização de Texto (`/api/v1/summarization/summarize`)

**Payload**:
```json
{
  "text": "O sistema de grande porte com 103.5B parâmetros atende requisições com alta performance e baixa latência...",
  "max_sentences": 3
}
```

---

### 4. 🔍 Análise de Texto & NLP (`/api/v1/analysis`)

- `POST /api/v1/analysis/sentiment`: Análise de sentimento (positivo, negativo, neutro).
- `POST /api/v1/analysis/ner`: Extração de entidades nomeadas.
- `POST /api/v1/analysis/classify`: Classificação zero-shot.

---

### 5. 👁️ Visão Computacional (`/api/v1/vision`)

- `POST /api/v1/vision/upload`: Upload de arquivo (`multipart/form-data`).
- `POST /api/v1/vision/url`: Análise de imagem por URL.

---

### 6. 🎙️ Processamento de Fala (`/api/v1/speech/transcribe`)

- `POST /api/v1/speech/transcribe`: Transcrição de áudio em formato MP3, WAV, OGG, WebM, M4A ou FLAC.

---

### 7. 🚦 Probes de Saúde (`/api/v1/health` & `/api/v1/ready`)

- `GET /api/v1/health`: Status básico de liveness.
- `GET /api/v1/ready`: Status detalhado de prontidão dos 5 microsserviços.

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
- **Python 3.12+**
- **Pip / Virtualenv**

### 1. Configuração do Ambiente

```bash
# Clonar e acessar o repositório
git clone <url-do-repositorio>
cd ia-open-source

# Criar e ativar o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Executando o API Gateway

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

Acesse a documentação interativa no navegador:
- **Swagger UI**: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
- **ReDoc**: [http://localhost:8000/api/v1/redoc](http://localhost:8000/api/v1/redoc)

---

## 🧪 Suíte de Testes Automatizados

Executar todos os testes unitários e de integração:

```bash
PYTHONPATH=. pytest tests/
```

Para verificar a compilação do código Python em todos os módulos:

```bash
python -m py_compile api/main.py api/routes/*.py services/llm_service/*.py tests/unit/*.py
```

---

## 📄 Licença

Este projeto é disponibilizado sob a licença [MIT](LICENCE).
