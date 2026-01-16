# Docker & Docker Compose - Compétences et Bonnes Pratiques

## Vue d'ensemble

Docker permet de containeriser l'application pour un déploiement reproductible. Docker Compose orchestre plusieurs conteneurs (app, database, redis, etc.).

## Dockerfile avec UV

### Dockerfile Multi-Stage (Production)

```dockerfile
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

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=40s \
    CMD curl -f http://localhost:8000/health || exit 1

# Commande par défaut
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Dockerfile.dev (Développement)

```dockerfile
FROM python:3.11-slim

# Installer UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances
COPY pyproject.toml uv.lock ./

# Installer TOUTES les dépendances (incluant dev)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --all-extras

# Copier le code source
COPY . .

EXPOSE 8000

# Commande avec reload pour dev
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

## Docker Compose

### docker-compose.yml (Base)

```yaml
version: "3.9"

services:
  # ============================================
  # APPLICATION PRINCIPALE
  # ============================================
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: langgraph-app
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "8000:8000"
    volumes:
      - ./src:/app/src:ro
      - ./secrets:/app/secrets:ro
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - langgraph-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # ============================================
  # WORKER CELERY
  # ============================================
  worker:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: langgraph-worker
    restart: unless-stopped
    command: celery -A src.worker worker --loglevel=info --concurrency=4
    env_file:
      - .env
    volumes:
      - ./src:/app/src:ro
      - ./secrets:/app/secrets:ro
    depends_on:
      - app
      - redis
    networks:
      - langgraph-network

  # ============================================
  # CELERY BEAT (Scheduler)
  # ============================================
  beat:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: langgraph-beat
    restart: unless-stopped
    command: celery -A src.worker beat --loglevel=info
    env_file:
      - .env
    volumes:
      - ./src:/app/src:ro
    depends_on:
      - worker
    networks:
      - langgraph-network

  # ============================================
  # POSTGRESQL
  # ============================================
  postgres:
    image: postgres:16-alpine
    container_name: langgraph-postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-langgraph_db}
      POSTGRES_USER: ${POSTGRES_USER:-langgraph_user}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-secure_password}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init_db.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - langgraph-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-langgraph_user} -d ${POSTGRES_DB:-langgraph_db}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ============================================
  # REDIS
  # ============================================
  redis:
    image: redis:7-alpine
    container_name: langgraph-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - langgraph-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ============================================
  # PGADMIN (Interface DB - Dev uniquement)
  # ============================================
  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: langgraph-pgadmin
    restart: unless-stopped
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - postgres
    networks:
      - langgraph-network
    profiles:
      - dev

  # ============================================
  # N8N (Optionnel - Automatisation)
  # ============================================
  n8n:
    image: n8nio/n8n:latest
    container_name: langgraph-n8n
    restart: unless-stopped
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=${N8N_USER:-admin}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD:-admin}
      - WEBHOOK_URL=${N8N_WEBHOOK_URL:-http://localhost:5678}
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n
    networks:
      - langgraph-network
    profiles:
      - automation

  # ============================================
  # QDRANT (Vector DB - Optionnel)
  # ============================================
  qdrant:
    image: qdrant/qdrant:latest
    container_name: langgraph-qdrant
    restart: unless-stopped
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage
    networks:
      - langgraph-network
    profiles:
      - vectordb

# ============================================
# VOLUMES
# ============================================
volumes:
  postgres_data:
  redis_data:
  n8n_data:
  qdrant_data:

# ============================================
# NETWORKS
# ============================================
networks:
  langgraph-network:
    driver: bridge
```

## Commandes Docker Compose

### Développement

```bash
# Démarrer tous les services
docker-compose up -d

# Démarrer avec profil dev (inclut pgadmin)
docker-compose --profile dev up -d

# Démarrer avec n8n
docker-compose --profile automation up -d

# Voir les logs
docker-compose logs -f app

# Logs en temps réel
docker-compose logs -f

# Reconstruire après modification
docker-compose up -d --build

# Arrêter tous les services
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v
```

### Production

```bash
# Build et push vers registry
docker build -t ghcr.io/username/langgraph-workflow:latest .
docker push ghcr.io/username/langgraph-workflow:latest

# Déployer
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## .dockerignore

```
# Git
.git
.gitignore
.github

# Python
__pycache__
*.py[cod]
*$py.class
.venv/
venv/
*.egg-info/

# UV - NE PAS IGNORER uv.lock
# uv.lock DOIT être inclus dans l'image

# Tests
tests/
.pytest_cache/
htmlcov/
.coverage

# Documentation
*.md
docs/

# IDE
.vscode/
.idea/
*.swp

# Environnement
.env
.env.*
!.env.example

# Secrets
secrets/
*.pem
*.key

# Notebooks
notebooks/
*.ipynb

# Logs
logs/
*.log

# Docker
Dockerfile.dev
docker-compose.override.yml
```

## Bonnes Pratiques

### 1. Multi-Stage Builds

- Stage 1 (builder): Installer les dépendances
- Stage 2 (runtime): Image finale minimale
- Réduire la taille de l'image de 50-70%

### 2. Cache Layers

```dockerfile
# ✅ Copier d'abord les dépendances (change rarement)
COPY pyproject.toml uv.lock ./
RUN uv sync

# ✅ Puis le code (change souvent)
COPY . .

# ❌ Ne pas copier tout en une fois
COPY . .
RUN uv sync
```

### 3. Health Checks

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### 4. Volumes

- **Named volumes** pour données persistantes (postgres_data, redis_data)
- **Bind mounts** pour développement (./src:/app/src)
- **Read-only** quand possible (:ro)

### 5. Réseaux

```yaml
networks:
  langgraph-network:
    driver: bridge
```

Tous les services sur le même réseau peuvent communiquer par nom de service.

### 6. Profiles

```yaml
profiles:
  - dev  # Seulement en dev
  - production  # Seulement en prod
```

```bash
docker-compose --profile dev up -d
```

### 7. Environment Variables

```yaml
environment:
  - POSTGRES_DB=${POSTGRES_DB:-langgraph_db}  # Avec valeur par défaut
env_file:
  - .env  # Charger depuis fichier
```

## Debugging

### Entrer dans un container

```bash
# Shell interactif
docker exec -it langgraph-app bash

# Exécuter une commande
docker exec langgraph-app uv run python -c "print('Hello')"
```

### Logs

```bash
# Tous les logs
docker-compose logs

# Service spécifique
docker-compose logs app

# Suivre en temps réel
docker-compose logs -f app

# Dernières 100 lignes
docker-compose logs --tail=100 app
```

### Inspection

```bash
# Stats des containers
docker stats

# Informations sur un container
docker inspect langgraph-app

# Réseau
docker network inspect langgraph-network
```

## Nettoyage

```bash
# Arrêter et supprimer les containers
docker-compose down

# Supprimer aussi les volumes
docker-compose down -v

# Supprimer les images
docker-compose down --rmi all

# Nettoyer tout Docker
docker system prune -af
docker volume prune -f
```

## Ressources

- Documentation Docker: https://docs.docker.com
- Documentation Compose: https://docs.docker.com/compose/
- Best practices: https://docs.docker.com/develop/dev-best-practices/

## Cas d'Usage du Projet

Docker est utilisé pour:

1. Containeriser l'application FastAPI
2. Orchestrer PostgreSQL et Redis
3. Déployer les workers Celery
4. Environnements de développement reproductibles
5. CI/CD et déploiement en production
6. Isolation des dépendances système
