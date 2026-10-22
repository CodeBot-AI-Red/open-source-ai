# 🤖 IA Open Source — Plataforma de Inteligência Artificial de Grande Porte

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

Uma plataforma de Inteligência Artificial de alta performance, modular, resiliente e escalável. O sistema é estruturado em arquitetura de microsserviços com um API Gateway baseado em **FastAPI** e serviços especializados descentralizados para **Processamento de Linguagem Natural (NLP)**, **Modelos de Linguagem de Grande Porte (LLM)**, **Visão Computacional**, **Processamento de Fala (Speech-to-Text)** e **Sumarização Automática**.

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
    +-----------------+--------------+--------------+------------------+
    |                 |              |              |                  |
    v                 v              v              v                  v
+-------+        +---------+    +----------+   +----------+     +--------------+
|  LLM  |        |   NLP   |    |  Vision  |   |  Speech  |     | Summarizer   |
|Service|        | Service |    | Service  |   | Service  |     |   Service    |
+-------+        +---------+    +----------+   +----------+     +--------------+
```

---

## ✨ Destaques & Recursos da Plataforma

- **Geração de Texto & Chat LLM Avançado**:
  - Suporte completo a parâmetros avançados de amostragem: `temperature`, `top_p`, `presence_penalty` e `frequency_penalty`.
  - Processamento automatizado de diretivas de sistema (`role: system`).
  - Streaming em tempo real via Server-Sent Events (SSE) `/chat/stream` e chunks NDJSON.
  - Backend determinístico inteligente com contabilidade detalhada de tokens (`prompt_tokens`, `completion_tokens`, `total_tokens`).
- **Segurança & Proteção de Prompts**:
  - Filtro avançado contra ataques de *prompt injection*, bypass de regras, exploração de modo DAN e exfiltração de segredos/tokens.
- **Processamento de Linguagem Natural (NLP)**:
  - Análise de sentimento com pontuação de confiança, reconhecimento de entidades nomeadas (NER) e classificação zero-shot de texto.
- **Visão Computacional**:
  - Suporte a upload direto de arquivos e análise via URL pública para classificação de imagens, detecção de faces e descrição visual.
- **Processamento de Fala (Speech-to-Text)**:
  - Transcrição de áudio multi-formato (MP3, WAV, OGG, WebM, M4A, FLAC) com auto-detecção de idioma e timestamps palavra por palavra.
- **Sumarização de Texto Resiliente**:
  - Algoritmo extrativo avançado com sistema de fallback automático em caso de indisponibilidade de serviços externos.
- **Pronto para Produção & Escalabilidade**:
  - Rastreabilidade ponta a ponta com middleware `X-Request-ID`.
  - Configuração distribuída via Docker Compose e manifestos Kubernetes (`/kubernetes`).

---

## 📚 Parâmetros & Documentação dos Endpoints

### 🔐 Autenticação
O API Gateway suporta dois métodos de autenticação configuráveis no cabeçalho `Authorization`:
- **JWT Token**: `Authorization: Bearer <token_jwt>`
- **API Key**: `Authorization: ApiKey <sua_api_key>`

---

### 1. 💬 Geração de Texto (LLM)

#### `POST /api/v1/generation/chat`
Envia o histórico de mensagens para o LLM e recebe uma resposta estruturada.

**Corpo da Requisição (`ChatRequest`)**:
| Parâmetro | Tipo | Padrão | Intervalo / Válidos | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `messages` | `list[ChatMessage]` | **Obrigatório** | Min: 1 item | Lista de mensagens da conversa. Cada item deve possuir `role` (`"system"`, `"user"`, `"assistant"`) e `content` (string). |
| `max_tokens` | `int` | `512` | `1` a `4096` | Limite máximo de tokens a serem gerados na resposta. |
| `temperature` | `float` | `0.7` | `0.0` a `2.0` | Controla a aleatoriedade da geração (valores mais altos tornam a saída mais criativa). |
| `top_p` | `float` | `1.0` | `0.0` a `1.0` | Amostragem Nucleus: considera tokens com massa de probabilidade top-p. |
| `presence_penalty` | `float` | `0.0` | `-2.0` a `2.0` | Penaliza tokens com base na sua presença no texto gerado até o momento. |
| `frequency_penalty` | `float` | `0.0` | `-2.0` a `2.0` | Penaliza tokens com base na sua frequência de repetição no texto gerado. |
| `stream` | `bool` | `false` | `true` / `false` | Se `true`, redireciona a requisição para o fluxo de streaming SSE. |

**Exemplo de Payload (`POST /api/v1/generation/chat`)**:
```json
{
  "messages": [
    {
      "role": "system",
      "content": "Você é um especialista em arquitetura de software de grande porte."
    },
    {
      "role": "user",
      "content": "Como organizar um projeto FastAPI modular em produção?"
    }
  ],
  "max_tokens": 256,
  "temperature": 0.7,
  "top_p": 0.9,
  "presence_penalty": 0.0,
  "frequency_penalty": 0.0,
  "stream": false
}
```

**Resposta de Exemplo (`ChatResponse`)**:
```json
{
  "id": "chatcmpl-a1b2c3d4e5f67890",
  "model": "open-source-ai-local-fallback-v2",
  "message": "[Diretiva do Sistema: Você é um especialista em arquitetura de software de grande porte.]\n\nPosso ajudar com isso. Uma abordagem segura é:\n1. Reproduzir o problema com um exemplo mínimo.\n2. Isolar entradas, saída esperada e saída real.\n3. Corrigir em pequenos passos com testes automatizados.\n4. Revisar logs e casos de borda.",
  "finish_reason": "stop",
  "usage": {
    "prompt_tokens": 32,
    "completion_tokens": 68,
    "total_tokens": 100
  }
}
```

---

#### `POST /api/v1/generation/chat/stream`
Inicia um fluxo contínuo de resposta token a token utilizando **Server-Sent Events (SSE)** (`text/event-stream`).
- **Parâmetros**: Mesmos parâmetros da rota `/chat`.
- **Formato do Evento**: Cada chunk é retornado com a estrutura `data: {"token": "..."}\n\n` e finalizado com `data: [DONE]\n\n`.

---

#### `POST /api/v1/generation/complete`
Gera a completação de um prompt textual simples.

**Corpo da Requisição (`CompletionRequest`)**:
| Parâmetro | Tipo | Padrão | Intervalo / Válidos | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `prompt` | `string` | **Obrigatório** | 1 a 8000 caracteres | Texto inicial para a completação. |
| `max_tokens` | `int` | `256` | `1` a `4096` | Limite máximo de tokens gerados. |
| `temperature` | `float` | `0.7` | `0.0` a `2.0` | Temperatura da geração. |
| `top_p` | `float` | `1.0` | `0.0` a `1.0` | Amostragem top-p. |
| `presence_penalty` | `float` | `0.0` | `-2.0` a `2.0` | Penalidade de presença. |
| `frequency_penalty` | `float` | `0.0` | `-2.0` a `2.0` | Penalidade de frequência. |

---

### 2. 📝 Sumarização de Texto (`/api/v1/summarization`)

#### `POST /api/v1/summarization/summarize`
Gera resumos sintéticos de textos extensos.

**Corpo da Requisição (`SummarizationRequest`)**:
| Parâmetro | Tipo | Padrão | Intervalo / Válidos | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `text` | `string` | **Obrigatório** | 1 a 20000 caracteres | Texto completo a ser sumarizado. |
| `max_sentences` | `int` | `5` | `1` a `20` | Quantidade máxima de frases no resumo final. |

**Resposta de Exemplo**:
```json
{
  "summary": "O sistema FastAPI oferece alta performance para sistemas de grande porte.",
  "sentences": [
    "O sistema FastAPI oferece alta performance para sistemas de grande porte."
  ],
  "model": "local-extractive-v1"
}
```

---

### 3. 🔍 Análise de Texto & NLP (`/api/v1/analysis`)

#### `POST /api/v1/analysis/sentiment`
Analisa a polaridade do sentimento de um texto.

| Parâmetro | Tipo | Padrão | Descrição |
| :--- | :--- | :--- | :--- |
| `text` | `string` | **Obrigatório** | Texto para análise (1 a 5000 caracteres). |
| `language` | `string` | `"pt"` | Código do idioma (ISO 639-1). |

#### `POST /api/v1/analysis/ner`
Extrai entidades nomeadas (Pessoas, Organizações, Locais, Diversos).

| Parâmetro | Tipo | Padrão | Descrição |
| :--- | :--- | :--- | :--- |
| `text` | `string` | **Obrigatório** | Texto para análise (1 a 5000 caracteres). |
| `entities` | `list[string]`| `["PER", "ORG", "LOC", "MISC"]` | Tipos de entidade a extrair. |

#### `POST /api/v1/analysis/classify`
Classificação de texto simples ou zero-shot.

| Parâmetro | Tipo | Padrão | Descrição |
| :--- | :--- | :--- | :--- |
| `text` | `string` | **Obrigatório** | Texto para análise (1 a 5000 caracteres). |
| `labels` | `list[string]`\|`null`| `null` | Rótulos candidatos para classificação zero-shot. |

---

### 4. 👁️ Visão Computacional (`/api/v1/vision`)

#### `POST /api/v1/vision/upload`
Upload de imagem via `multipart/form-data`.
- **Form Data**: `file` (JPEG, PNG, WebP, GIF; até 25 MB).
- **Query Param**: `task` (`"classify"`, `"detect_faces"`, `"describe"`, padrão: `"classify"`).

#### `POST /api/v1/vision/url`
Análise de imagem via URL pública.
- **Body**: `{"url": "https://exemplo.com/imagem.jpg", "task": "classify"}`

---

### 5. 🎙️ Processamento de Fala (`/api/v1/speech`)

#### `POST /api/v1/speech/transcribe`
Transcrição de arquivos de áudio para texto.
- **Form Data**:
  - `file`: Arquivo de áudio (MP3, WAV, OGG, WebM, M4A, FLAC; até 25 MB).
  - `language`: (Opcional) Código ISO do idioma. Se omitido, auto-detecta.
  - `return_timestamps`: (Opcional, `bool`, padrão: `false`) Retorna marcas temporais de palavras.

---

### 6. 🚦 Probes de Saúde (`/api/v1/health` & `/api/v1/ready`)

- `GET /api/v1/health`: Liveness probe do Kubernetes.
- `GET /api/v1/ready`: Readiness probe que checa a latência e status de todos os 5 microsserviços.

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
- **Python 3.12+**
- **Virtualenv**

### 1. Configuração do Ambiente

```bash
# Clonar e acessar o repositório
git clone <url-do-repositorio>
cd ia-open-source

# Criar e ativar o ambiente virtual
python -m venv .venv
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

### 3. Executando Microsserviços Individuais

Para rodar o serviço LLM isoladamente:

```bash
uvicorn services.llm_service.inference:app --host 0.0.0.0 --port 8002 --reload
```

---

## 🧪 Suíte de Testes Automatizados

Executar todos os testes unitários e de integração:

```bash
PYTHONPATH=. pytest
```

Para verificar a compilação de código Python em todos os módulos:

```bash
python -m py_compile api/main.py api/routes/*.py services/llm_service/*.py tests/unit/*.py
```

---

## 🛡️ Variáveis de Ambiente & Configuração

As configurações principais podem ser ajustadas via arquivo `.env` ou variáveis de ambiente:

| Variável | Padrão | Descrição |
| :--- | :--- | :--- |
| `ENVIRONMENT` | `development` | Ambiente (`development`, `staging`, `production`). |
| `LOG_LEVEL` | `INFO` | Nível de log (`DEBUG`, `INFO`, `WARNING`, `ERROR`). |
| `SECRET_KEY` | *(Secret)* | Chave secreta para assinatura JWT. |
| `RATE_LIMIT_ENABLED` | `true` | Ativa/desativa rate limiting. |
| `RATE_LIMIT_REQUESTS` | `60` | Número de requisições permitidas por janela. |
| `LLM_SERVICE_URL` | `http://llm_service:8002` | URL do serviço LLM interno. |
| `NLP_SERVICE_URL` | `http://nlp_service:8001` | URL do serviço NLP interno. |
| `VISION_SERVICE_URL` | `http://vision_service:8003` | URL do serviço de Visão interno. |
| `SPEECH_SERVICE_URL` | `http://speech_service:8004` | URL do serviço de Fala interno. |
| `SUMMARIZER_SERVICE_URL` | `http://summarizer_service:8005` | URL do serviço de Sumarização interno. |

---

## 📄 Licença

Este projeto é disponibilizado sob a licença [MIT](LICENCE).
