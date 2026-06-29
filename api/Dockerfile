# api/Dockerfile
# ─────────────────────────────────────────────────────────────────────────────
# Estágio 1: build das dependências
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

# Instala dependências de sistema necessárias para compilar pacotes nativos
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instala as dependências Python em um diretório isolado
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt

# ─────────────────────────────────────────────────────────────────────────────
# Estágio 2: imagem final mínima
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

# Variáveis de ambiente de segurança e performance
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=8000

WORKDIR /app

# Copia dependências instaladas do builder
COPY --from=builder /install /usr/local

# Copia apenas o código da API (não inclui testes, notebooks, etc.)
COPY . /app/api

# Cria usuário sem privilégios para executar a aplicação
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

EXPOSE $PORT

# Healthcheck para o Docker / Kubernetes
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# Uvicorn com múltiplos workers (ajuste --workers conforme os CPUs disponíveis)
CMD ["sh", "-c", \
     "uvicorn api.main:app --host 0.0.0.0 --port $PORT --workers 2 --log-level info"]
