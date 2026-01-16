# ============================================ 
# STAGE 1: Builder avec UV 
# ============================================ 
FROM python:3.11-slim AS builder

# Installer UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Variables d'environnement
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

# Copier les fichiers de dépendances
COPY pyproject.toml uv.lock ./

# Installer les dépendances (sans le projet lui-même)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copier le code source
COPY . .

# Installer le projet
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ============================================ 
# STAGE 2: Runtime 
# ============================================ 
FROM python:3.11-slim AS runtime

# Métadonnées
LABEL maintainer="your-email@domain.com"
LABEL description="LangGraph Workflows Boilerplate"

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    PATH="/app/.venv/bin:$PATH"

# Répertoire de travail
WORKDIR /app

# Dépendances système minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier l'environnement virtuel depuis le builder
COPY --from=builder /app/.venv /app/.venv

# Copier le code source
COPY --from=builder /app/src /app/src

# Port par défaut
EXPOSE 8000

# Commande par défaut
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
