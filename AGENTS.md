
> **Document de référence pour tout agent IA travaillant sur ce boilerplate**
> Ce fichier contient toutes les directives techniques pour initialiser et développer des projets d'automatisation et workflows agentiques.

---

**Instructions pour l'Agent Utilisé**

> Ce fichier est à **copier/coller** puis le supprimer, dans l'un de ces fichiers selon le LLM utilisé : 
- Claude-Code : CLAUDE.md,
- Gemini-CLI : GEMINI.md,
- Others : AGENTS.md,

Afin que les mêmes instructions se chargent dans n'importe quel environnement d'IA.

**Contenu à copier/coller**

# Mémoire Agent IA

## Table des Matières

1. [Vue d'ensemble du Projet](#vue-densemble-du-projet)
2. [Stack Technologique](#stack-technologique)
3. [Structure du Projet](#structure-du-projet)
4. [Configuration Initiale](#configuration-initiale) *(inclut installation UV)*
5. [Docker & Docker Compose](#docker--docker-compose)
6. [Base de Données PostgreSQL](#base-de-données-postgresql)
7. [LangChain & LangGraph](#langchain--langgraph)
8. [Intégrations API](#intégrations-api)
9. [Gestion des Secrets](#gestion-des-secrets)
10. [GitHub & CI/CD](#github--cicd) *(inclut commandes gh)*
11. [Conventions de Code](#conventions-de-code)
12. [Commandes Utiles](#commandes-utiles) *(inclut commandes UV)*

---

## Vue d'ensemble du Projet

Ce boilerplate est conçu pour créer des **workflows agentiques** et des **automatisations intelligentes** utilisant l'écosystème LangChain/LangGraph. Il permet de construire des agents IA autonomes capables d'interagir avec de multiples services externes.

### Objectifs Principaux
- Automatisation de tâches complexes via agents IA
- Orchestration de workflows multi-étapes avec LangGraph
- Intégration transparente avec les APIs tierces
- Déploiement containerisé et reproductible
- Persistance des états et checkpoints

---

## Stack Technologique

### Core
| Technologie | Version Minimale | Usage |
|-------------|------------------|-------|
| Python | 3.11+ | Langage principal |
| **UV (Astral)** | **0.5+** | **Gestionnaire de paquets Python (OBLIGATOIRE)** |
| **GitHub CLI (gh)** | **2.40+** | **Opérations GitHub/CI/CD (OBLIGATOIRE)** |
| LangChain | 0.3+ | Framework agents/chains |
| LangGraph | 0.2+ | Orchestration workflows |
| PostgreSQL | 15+ | Base de données principale |
| Docker | 24+ | Containerisation |
| Docker Compose | 2.20+ | Orchestration containers |

> **IMPORTANT**: Ce projet utilise **exclusivement UV** comme gestionnaire de paquets Python. Ne jamais utiliser pip, pipenv, poetry ou conda directement. UV est un outil ultra-rapide écrit en Rust par Astral (les créateurs de Ruff).

> **IMPORTANT**: Toutes les opérations GitHub (repos, PRs, issues, workflows, releases) doivent être effectuées via **GitHub CLI (gh)**. Ne pas utiliser l'interface web ou d'autres outils.

### Dépendances Python Essentielles
```
langchain>=0.3.0
langchain-core>=0.3.0
langchain-community>=0.3.0
langgraph>=0.2.0
langgraph-checkpoint-postgres>=0.1.0
langchain-openai>=0.2.0
langchain-anthropic>=0.2.0
langchain-google-genai>=2.0.0
langsmith>=0.1.0
psycopg[binary]>=3.1.0
asyncpg>=0.29.0
sqlalchemy>=2.0.0
alembic>=1.13.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
python-dotenv>=1.0.0
httpx>=0.27.0
aiohttp>=3.9.0
redis>=5.0.0
celery>=5.3.0
```

---

## Structure du Projet

```
C:\Users\rabia\Workspace\langgraph-workflows-boilerplate\
├── CLAUDE_OR_GEMINI_OR_AGENTS.md  # CE FICHIER - Mémoire Agent IA
├── README.md                     # Documentation projet
├── .ai/                          # 🧠 Intelligence Artificielle & Mémoire
│   ├── agents/                   # Rôles et instructions IA (Markdown)
│   ├── commands/                 # Workflows opérationnels / Playbooks (Markdown)
│   ├── shared-context/           # Base de connaissances et état du projet (Markdown)
│   └── skills/                   # Expertise technique et patterns (Markdown)
├── .env.example                  # Template variables d'environnement
├── .env                          # Variables d'environnement (GITIGNORE)
├── .gitignore                    # Fichiers ignorés par Git
├── .python-version               # Version Python pour UV
├── docker-compose.yml            # Orchestration Docker
├── docker-compose.dev.yml        # Override développement
├── docker-compose.prod.yml       # Override production
├── Dockerfile                    # Image principale
├── pyproject.toml                # Configuration projet Python (UV)
├── uv.lock                       # Lockfile UV (TOUJOURS COMMITER)
├── alembic.ini                   # Configuration migrations DB
│
├── src/                          # Code source principal
│   ├── __init__.py
│   ├── main.py                   # Point d'entrée application
│   ├── config/                   # Configuration
│   │   ├── __init__.py
│   │   ├── settings.py           # Settings Pydantic
│   │   └── logging.py            # Configuration logs
│   │
│   ├── agents/                   # Agents LangGraph
│   │   ├── __init__.py
│   │   ├── base.py               # Agent de base
│   │   └── workflows/            # Workflows spécifiques
│   │       ├── __init__.py
│   │       └── example_workflow.py
│   │
│   ├── graphs/                   # Définitions LangGraph
│   │   ├── __init__.py
│   │   ├── nodes.py              # Nœuds du graphe
│   │   ├── edges.py              # Conditions de transition
│   │   └── state.py              # États du graphe
│   │
│   ├── chains/                   # Chains LangChain
│   │   ├── __init__.py
│   │   └── base_chains.py
│   │
│   ├── tools/                    # Outils pour agents
│   │   ├── __init__.py
│   │   ├── base.py               # Tool de base
│   │   ├── google/               # Outils Google
│   │   │   ├── __init__.py
│   │   │   ├── drive.py
│   │   │   ├── gmail.py
│   │   │   └── sheets.py
│   │   ├── notion/
│   │   │   ├── __init__.py
│   │   │   └── client.py
│   │   ├── messaging/            # WhatsApp, Telegram
│   │   │   ├── __init__.py
│   │   │   ├── whatsapp.py
│   │   │   └── telegram.py
│   │   └── integrations/         # Autres intégrations
│   │       ├── __init__.py
│   │       ├── n8n.py
│   │       └── reranker.py
│   │
│   ├── prompts/                  # Templates de prompts
│   │   ├── __init__.py
│   │   └── templates/
│   │       └── base.yaml
│   │
│   ├── models/                   # Modèles SQLAlchemy
│   │   ├── __init__.py
│   │   └── base.py
│   │
│   ├── schemas/                  # Schémas Pydantic
│   │   ├── __init__.py
│   │   └── base.py
│   │
│   ├── services/                 # Services métier
│   │   ├── __init__.py
│   │   └── base.py
│   │
│   ├── api/                      # API FastAPI (optionnel)
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── routes/
│   │       └── __init__.py
│   │
│   └── utils/                    # Utilitaires
│       ├── __init__.py
│       ├── helpers.py
│       └── decorators.py
│
├── migrations/                   # Migrations Alembic
│   ├── env.py
│   └── versions/
│
├── tests/                        # Tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   └── integration/
│
├── scripts/                      # Scripts utilitaires
│   ├── init_db.py
│   └── seed_data.py
│
└── notebooks/                    # Jupyter notebooks (dev/exploration)
    └── exploration.ipynb
```

---

## Utilisation de la Mémoire Locale (Agents, Commands, Skills & Shared Context)

> **DIRECTIVE CRITIQUE ET OBLIGATOIRE** : Pour garantir la continuité du projet et éviter la perte de contexte, tout agent (Main ou Sub-Agent) **DOIT** suivre le protocole de mémoire locale.

### 🔴 PROTOCOLE DE SESSION (OBLIGATOIRE)

1.  **AU DÉBUT DE LA TÂCHE** : Consulter impérativement `@.ai/shared-context/session-active.md`. L'agent doit baser ses actions sur l'état actuel et les dernières actions documentées.
2.  **PANDANT LA TÂCHE** : Se référer aux `@.ai/skills/` pour l'implémentation technique et aux `@.ai/commands/` pour la méthodologie (ex: EPCT).
3.  **À LA FIN DE LA TÂCHE** : Mettre à jour systématiquement `@.ai/shared-context/session-active.md` (unique fichier d'avancement).

### 1. Dossier `@.ai/shared-context/` (Contexte & État)
C'est la **mémoire unique** du projet.
- **RÈGLE CRITIQUE** : Tout l'avancement, les décisions et l'état du projet **DOIVENT** être consignés exclusivement dans `session-active.md`.
- **INTERDICTION** : Ne jamais créer d'autres fichiers (ex: `PROJECT_STATUS.md`, `DECISION_LOG.md`, etc.). S'ils existent, ils doivent être supprimés et leur contenu fusionné dans `session-active.md`.
- **EXCEPTION** : La création de nouveaux fichiers dans ce dossier est strictement réservée à une demande explicite de l'utilisateur.
- **Action** : Respectez scrupuleusement `rules.md` pour la mise à jour de `session-active.md`.

### 2. Dossier `@.ai/commands/` (Playbooks Opérationnels)
Contient des séquences d'actions pas à pas pour des tâches spécifiques.
**Commandes disponibles :**
- `debug.md` : Protocole de débogage et résolution d'erreurs.
- `epct.md` : (Explore, Plan, Code, Test) Workflow standard de développement.

### 3. Dossier `@.ai/skills/` (Expertise Technique)
Contient la documentation technique approfondie et les **patterns de code validés** pour chaque technologie.
**Compétences disponibles :**
- `cohere-api.md`
- `docker.md`
- `fastapi.md`
- `google-apis.md`
- `integrations.md`
- `langchain.md`
- `langgraph.md`
- `n8n.md`
- `notion-api.md`
- `postgresql-sqlalchemy.md`
- `pydantic.md`
- `telegram-api.md`
- `uv.md`
- `whatsapp-api.md`

- **Action :** Si vous devez intégrer une API ou utiliser une techno listée ci-dessus, lisez d'abord le fichier correspondant dans `@.ai/skills/`.

### 4. Dossier `@.ai/agents/` (Sous-Agents Spécialisés)
Contient des définitions de rôles et des instructions spécifiques.
**Agents disponibles :**
- `codebase-explorer-expert.md` : Expert en exploration et compréhension du code.
- `devops-expert.md` : Expert en déploiement, Docker, CI/CD.
- `langgraph-architect-expert.md` : Architecte spécialisé LangGraph.
- `n8n-convertor-expert.md` : Expert migration et conversion n8n.
- `prompt-engineer-expert.md` : Expert en conception de prompts.
- `python-developer-expert.md` : Développeur Python expert.
- `security-reviewer-expert.md` : Expert en audit de sécurité.
- `testing-expert.md` : Expert en tests unitaires et intégration.

- **Action :** Référez-vous à l'agent approprié pour des tâches spécialisées.
- **Délégation (Main Agent) :** Lorsqu'un agent principal délègue une tâche à un sous-agent, il doit impérativement lui préciser l'objectif clair de la tâche ET les éventuels sub-agents à solliciter si nécessaire.

### 5. Avantages de cette approche
- **Zéro Redondance :** On ne réinvente pas la roue à chaque session.
- **Économie de Tokens :** En lisant des fichiers ciblés, on évite de charger tout l'historique de chat.
- **Alignement Parfait :** Tous les agents travaillent vers le même objectif avec les mêmes règles.

---

## Configuration Initiale

### Prérequis: Installation des Outils Obligatoires

#### 1. UV (Gestionnaire de paquets Python)

UV est **obligatoire** pour ce projet. Installer UV avant toute chose:

```bash
# Installation UV (Windows PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Installation UV (Linux/macOS)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Vérifier l'installation
uv --version
```

#### 2. GitHub CLI (gh)

GitHub CLI est **obligatoire** pour toutes les opérations GitHub/CI/CD:

```bash
# Installation gh (Windows - winget)
winget install GitHub.cli

# Installation gh (Windows - Scoop)
scoop install gh

# Installation gh (macOS - Homebrew)
brew install gh

# Installation gh (Linux - apt)
sudo apt install gh

# Installation gh (Linux - dnf)
sudo dnf install gh

# Authentification (OBLIGATOIRE après installation)
gh auth login

# Vérifier l'installation
gh --version
```

> **Note**: L'authentification `gh auth login` est requise une seule fois. Choisir l'authentification via navigateur ou token.

### Étape 1: Cloner et Configurer l'Environnement

```bash
# Cloner le repository
git clone <repository-url>
cd langgraph-workflows-boilerplate

# Copier le fichier d'environnement
cp .env.example .env

# Éditer .env avec vos clés API

# Créer l'environnement virtuel et installer les dépendances avec UV
uv sync

# Ou avec les dépendances de développement
uv sync --all-extras
```

### Étape 2: Fichier .env.example

```env
# ============================================
# APPLICATION
# ============================================
APP_NAME=langgraph-workflow
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO

# ============================================
# BASE DE DONNÉES
# ============================================
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=langgraph_db
POSTGRES_USER=langgraph_user
POSTGRES_PASSWORD=secure_password_here
DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

# ============================================
# REDIS (pour Celery et cache)
# ============================================
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_URL=redis://${REDIS_HOST}:${REDIS_PORT}/0
CELERY_BROKER_URL=redis://${REDIS_HOST}:${REDIS_PORT}/1
CELERY_RESULT_BACKEND=redis://${REDIS_HOST}:${REDIS_PORT}/2

# ============================================
# LLM PROVIDERS
# ============================================
# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Google AI
GOOGLE_API_KEY=...
GOOGLE_MODEL=gemini-1.5-pro

# ============================================
# LANGSMITH (Observabilité)
# ============================================
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=ls__...
LANGCHAIN_PROJECT=langgraph-workflow

# ============================================
# GOOGLE WORKSPACE APIs
# ============================================
# Chemin vers le fichier credentials OAuth2
GOOGLE_CREDENTIALS_PATH=/app/secrets/google_credentials.json
GOOGLE_TOKEN_PATH=/app/secrets/google_token.json

# Service Account (alternative)
GOOGLE_SERVICE_ACCOUNT_PATH=/app/secrets/service_account.json

# Scopes requis (séparés par virgule)
GOOGLE_SCOPES=https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/spreadsheets

# ============================================
# NOTION
# ============================================
NOTION_API_KEY=secret_...
NOTION_VERSION=2022-06-28
NOTION_DATABASE_ID=...

# ============================================
# WHATSAPP (Meta Business API)
# ============================================
WHATSAPP_PHONE_NUMBER_ID=...
WHATSAPP_BUSINESS_ACCOUNT_ID=...
WHATSAPP_ACCESS_TOKEN=...
WHATSAPP_VERIFY_TOKEN=...
WHATSAPP_WEBHOOK_URL=https://your-domain.com/webhook/whatsapp

# ============================================
# TELEGRAM
# ============================================
TELEGRAM_BOT_TOKEN=...
TELEGRAM_WEBHOOK_URL=https://your-domain.com/webhook/telegram
TELEGRAM_CHAT_ID=...

# ============================================
# N8N
# ============================================
N8N_BASE_URL=http://n8n:5678
N8N_API_KEY=...
N8N_WEBHOOK_URL=...

# ============================================
# COHERE (Reranker)
# ============================================
COHERE_API_KEY=...
COHERE_RERANK_MODEL=rerank-english-v3.0

# ============================================
# SLACK
# ============================================
SLACK_BOT_TOKEN=xoxb-...
SLACK_SIGNING_SECRET=...
SLACK_APP_TOKEN=xapp-...

# ============================================
# GITHUB
# ============================================
GITHUB_TOKEN=ghp_...
GITHUB_WEBHOOK_SECRET=...

# ============================================
# AIRTABLE
# ============================================
AIRTABLE_API_KEY=pat...
AIRTABLE_BASE_ID=app...

# ============================================
# HUBSPOT
# ============================================
HUBSPOT_API_KEY=...
HUBSPOT_ACCESS_TOKEN=...

# ============================================
# ZAPIER
# ============================================
ZAPIER_WEBHOOK_URL=...
ZAPIER_NLA_API_KEY=...

# ============================================
# TWILIO (SMS/Voice)
# ============================================
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=...

# ============================================
# SENDGRID (Email)
# ============================================
SENDGRID_API_KEY=SG...

# ============================================
# STRIPE
# ============================================
STRIPE_API_KEY=sk_...
STRIPE_WEBHOOK_SECRET=whsec_...

# ============================================
# AWS
# ============================================
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=eu-west-1
AWS_S3_BUCKET=...

# ============================================
# PINECONE (Vector DB)
# ============================================
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=...
PINECONE_INDEX_NAME=...

# ============================================
# QDRANT (Vector DB Alternative)
# ============================================
QDRANT_HOST=qdrant
QDRANT_PORT=6333
QDRANT_API_KEY=...

# ============================================
# SUPABASE
# ============================================
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...

# ============================================
# DISCORD
# ============================================
DISCORD_BOT_TOKEN=...
DISCORD_GUILD_ID=...

# ============================================
# CALENDLY
# ============================================
CALENDLY_API_KEY=...

# ============================================
# JIRA
# ============================================
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=...
JIRA_API_TOKEN=...

# ============================================
# LINEAR
# ============================================
LINEAR_API_KEY=lin_api_...

# ============================================
# MONDAY.COM
# ============================================
MONDAY_API_KEY=...
```

### Étape 3: Configuration Python (pyproject.toml) - Compatible UV

```toml
[project]
name = "langgraph-workflow"
version = "0.1.0"
description = "Boilerplate pour workflows agentiques LangGraph"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    # Core LangChain/LangGraph
    "langchain>=0.3.0",
    "langchain-core>=0.3.0",
    "langchain-community>=0.3.0",
    "langgraph>=0.2.0",
    "langgraph-checkpoint-postgres>=0.1.0",

    # LLM Providers
    "langchain-openai>=0.2.0",
    "langchain-anthropic>=0.2.0",
    "langchain-google-genai>=2.0.0",
    "langchain-cohere>=0.3.0",

    # Observabilité
    "langsmith>=0.1.0",

    # Database
    "psycopg[binary]>=3.1.0",
    "asyncpg>=0.29.0",
    "sqlalchemy[asyncio]>=2.0.0",
    "alembic>=1.13.0",

    # API Framework
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",

    # Validation
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",

    # HTTP
    "httpx>=0.27.0",
    "aiohttp>=3.9.0",

    # Task Queue
    "redis>=5.0.0",
    "celery>=5.3.0",

    # Utils
    "python-dotenv>=1.0.0",
    "structlog>=24.0.0",
    "tenacity>=8.2.0",

    # Google APIs
    "google-api-python-client>=2.100.0",
    "google-auth-httplib2>=0.2.0",
    "google-auth-oauthlib>=1.2.0",

    # Autres intégrations
    "notion-client>=2.2.0",
    "python-telegram-bot>=21.0",
    "slack-sdk>=3.27.0",
    "cohere>=5.0.0",
    "tweepy>=4.14.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.12.0",
    "ruff>=0.4.0",
    "mypy>=1.10.0",
    "pre-commit>=3.7.0",
    "ipython>=8.0.0",
    "jupyter>=1.0.0",
]

# ============================================
# CONFIGURATION UV (Astral)
# ============================================
[tool.uv]
# Utiliser le resolver UV
dev-dependencies = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.12.0",
    "ruff>=0.4.0",
    "mypy>=1.10.0",
    "pre-commit>=3.7.0",
    "ipython>=8.0.0",
    "jupyter>=1.0.0",
]

[tool.uv.sources]
# Sources personnalisées si nécessaire
# langchain = { git = "https://github.com/langchain-ai/langchain.git" }

# ============================================
# CONFIGURATION OUTILS
# ============================================
[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "SIM"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.11"
strict = true
ignore_missing_imports = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

### Fichier .python-version

```
3.11
```

> **Note**: Ce fichier indique à UV quelle version de Python utiliser. UV peut automatiquement télécharger et gérer cette version.

---

## Docker & Docker Compose

### Dockerfile (avec UV)

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

# Commande par défaut
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Dockerfile.dev (pour développement avec UV)

```dockerfile
FROM python:3.11-slim

# Installer UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Métadonnées
LABEL maintainer="your-email@domain.com"
LABEL description="LangGraph Workflows Boilerplate - Dev"

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Répertoire de travail
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

# Port par défaut
EXPOSE 8000

# Commande par défaut (avec reload pour dev)
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### docker-compose.yml

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

### Commandes Docker

```bash
# Démarrer tous les services
docker-compose up -d

# Démarrer avec profil dev (inclut pgadmin)
docker-compose --profile dev up -d

# Démarrer avec n8n
docker-compose --profile automation up -d

# Voir les logs
docker-compose logs -f app

# Reconstruire après modification
docker-compose up -d --build

# Arrêter tous les services
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v
```

---

## Base de Données PostgreSQL

### Configuration Checkpointer LangGraph

```python
# src/config/database.py
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config.settings import settings

# Engine SQLAlchemy async
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=5,
    max_overflow=10,
)

# Session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Checkpointer LangGraph
async def get_checkpointer() -> AsyncPostgresSaver:
    """Retourne un checkpointer PostgreSQL pour LangGraph."""
    checkpointer = AsyncPostgresSaver.from_conn_string(
        settings.DATABASE_URL.replace("+asyncpg", "")
    )
    await checkpointer.setup()
    return checkpointer
```

### Script d'Initialisation DB

```sql
-- scripts/init_db.sql

-- Extension pour UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Extension pour recherche full-text
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Extension pour vecteurs (si pgvector installé)
-- CREATE EXTENSION IF NOT EXISTS "vector";

-- Table pour les checkpoints LangGraph (créée automatiquement par LangGraph)
-- Mais on peut créer des tables métier ici

-- Table exemple: Workflow Runs
CREATE TABLE IF NOT EXISTS workflow_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    thread_id VARCHAR(255) NOT NULL,
    workflow_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    input_data JSONB,
    output_data JSONB,
    error_message TEXT,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index pour recherche rapide
CREATE INDEX IF NOT EXISTS idx_workflow_runs_thread_id ON workflow_runs(thread_id);
CREATE INDEX IF NOT EXISTS idx_workflow_runs_status ON workflow_runs(status);
CREATE INDEX IF NOT EXISTS idx_workflow_runs_workflow_name ON workflow_runs(workflow_name);

-- Table pour les logs d'intégration
CREATE TABLE IF NOT EXISTS integration_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    integration_name VARCHAR(100) NOT NULL,
    action VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    request_data JSONB,
    response_data JSONB,
    error_message TEXT,
    duration_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_integration_logs_name ON integration_logs(integration_name);
CREATE INDEX IF NOT EXISTS idx_integration_logs_created_at ON integration_logs(created_at);
```

---

## LangChain & LangGraph

### Configuration Settings

```python
# src/config/settings.py
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    """Configuration centralisée de l'application."""

    # Application
    APP_NAME: str = "langgraph-workflow"
    APP_ENV: str = "development"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # LLM Providers
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4-turbo-preview"

    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"

    GOOGLE_API_KEY: Optional[str] = None
    GOOGLE_MODEL: str = "gemini-1.5-pro"

    # LangSmith
    LANGCHAIN_TRACING_V2: bool = True
    LANGCHAIN_API_KEY: Optional[str] = None
    LANGCHAIN_PROJECT: str = "langgraph-workflow"

    # APIs
    NOTION_API_KEY: Optional[str] = None
    COHERE_API_KEY: Optional[str] = None
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    WHATSAPP_ACCESS_TOKEN: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

### Structure d'un Graph LangGraph

```python
# src/graphs/state.py
from typing import TypedDict, Annotated, List, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """État partagé du graphe."""
    messages: Annotated[List[BaseMessage], add_messages]
    current_step: str
    context: dict
    error: Optional[str]
    final_output: Optional[dict]


# src/graphs/nodes.py
from langchain_core.messages import AIMessage, HumanMessage
from src.graphs.state import AgentState

async def analyze_input(state: AgentState) -> AgentState:
    """Nœud d'analyse de l'entrée."""
    # Logique d'analyse
    return {
        **state,
        "current_step": "analyzed",
        "context": {"analyzed": True}
    }

async def process_task(state: AgentState) -> AgentState:
    """Nœud de traitement principal."""
    # Logique de traitement
    return {
        **state,
        "current_step": "processed"
    }

async def generate_output(state: AgentState) -> AgentState:
    """Nœud de génération de sortie."""
    return {
        **state,
        "current_step": "completed",
        "final_output": {"result": "success"}
    }


# src/graphs/edges.py
from src.graphs.state import AgentState

def should_continue(state: AgentState) -> str:
    """Détermine la prochaine étape."""
    if state.get("error"):
        return "error_handler"
    if state["current_step"] == "analyzed":
        return "process"
    return "end"


# src/agents/workflows/example_workflow.py
from langgraph.graph import StateGraph, END
from src.graphs.state import AgentState
from src.graphs.nodes import analyze_input, process_task, generate_output
from src.graphs.edges import should_continue
from src.config.database import get_checkpointer

async def create_workflow():
    """Crée et retourne le workflow compilé."""

    # Définir le graphe
    workflow = StateGraph(AgentState)

    # Ajouter les nœuds
    workflow.add_node("analyze", analyze_input)
    workflow.add_node("process", process_task)
    workflow.add_node("generate", generate_output)

    # Définir les transitions
    workflow.set_entry_point("analyze")
    workflow.add_conditional_edges(
        "analyze",
        should_continue,
        {
            "process": "process",
            "error_handler": END,
        }
    )
    workflow.add_edge("process", "generate")
    workflow.add_edge("generate", END)

    # Compiler avec checkpointer
    checkpointer = await get_checkpointer()
    return workflow.compile(checkpointer=checkpointer)
```

### Exemple d'Utilisation

```python
# src/main.py
import asyncio
from uuid import uuid4
from langchain_core.messages import HumanMessage
from src.agents.workflows.example_workflow import create_workflow

async def main():
    # Créer le workflow
    app = await create_workflow()

    # Configuration du thread
    thread_id = str(uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    # Exécuter
    initial_state = {
        "messages": [HumanMessage(content="Traite cette tâche")],
        "current_step": "start",
        "context": {},
        "error": None,
        "final_output": None,
    }

    result = await app.ainvoke(initial_state, config)
    print(f"Résultat: {result['final_output']}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Intégrations API

### Google Workspace (Drive, Gmail, Sheets)

```python
# src/tools/google/auth.py
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
from src.config.settings import settings

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/spreadsheets',
]

def get_google_credentials():
    """Obtient les credentials Google (OAuth2 ou Service Account)."""

    # Option 1: Service Account
    if settings.GOOGLE_SERVICE_ACCOUNT_PATH:
        return service_account.Credentials.from_service_account_file(
            settings.GOOGLE_SERVICE_ACCOUNT_PATH,
            scopes=SCOPES
        )

    # Option 2: OAuth2
    creds = None
    token_path = settings.GOOGLE_TOKEN_PATH

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                settings.GOOGLE_CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds


# src/tools/google/drive.py
from langchain_core.tools import tool
from googleapiclient.discovery import build
from src.tools.google.auth import get_google_credentials

@tool
def list_drive_files(folder_id: str = "root", max_results: int = 10) -> list:
    """Liste les fichiers dans un dossier Google Drive.

    Args:
        folder_id: ID du dossier (défaut: root)
        max_results: Nombre max de résultats

    Returns:
        Liste des fichiers avec id, name, mimeType
    """
    creds = get_google_credentials()
    service = build('drive', 'v3', credentials=creds)

    results = service.files().list(
        q=f"'{folder_id}' in parents",
        pageSize=max_results,
        fields="files(id, name, mimeType, createdTime)"
    ).execute()

    return results.get('files', [])

@tool
def upload_to_drive(file_path: str, folder_id: str = None) -> dict:
    """Upload un fichier vers Google Drive."""
    from googleapiclient.http import MediaFileUpload

    creds = get_google_credentials()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': os.path.basename(file_path)}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(file_path)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name, webViewLink'
    ).execute()

    return file


# src/tools/google/gmail.py
from langchain_core.tools import tool
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

@tool
def send_email(to: str, subject: str, body: str) -> dict:
    """Envoie un email via Gmail.

    Args:
        to: Adresse email du destinataire
        subject: Sujet de l'email
        body: Corps du message

    Returns:
        Informations sur l'email envoyé
    """
    creds = get_google_credentials()
    service = build('gmail', 'v1', credentials=creds)

    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    sent = service.users().messages().send(
        userId='me',
        body={'raw': raw}
    ).execute()

    return sent

@tool
def search_emails(query: str, max_results: int = 10) -> list:
    """Recherche des emails dans Gmail."""
    creds = get_google_credentials()
    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(
        userId='me',
        q=query,
        maxResults=max_results
    ).execute()

    messages = results.get('messages', [])

    detailed = []
    for msg in messages:
        detail = service.users().messages().get(
            userId='me',
            id=msg['id']
        ).execute()
        detailed.append(detail)

    return detailed


# src/tools/google/sheets.py
@tool
def read_spreadsheet(spreadsheet_id: str, range_name: str) -> list:
    """Lit des données depuis Google Sheets.

    Args:
        spreadsheet_id: ID du spreadsheet
        range_name: Plage à lire (ex: "Sheet1!A1:D10")

    Returns:
        Liste des valeurs
    """
    creds = get_google_credentials()
    service = build('sheets', 'v4', credentials=creds)

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_name
    ).execute()

    return result.get('values', [])

@tool
def write_spreadsheet(spreadsheet_id: str, range_name: str, values: list) -> dict:
    """Écrit des données dans Google Sheets."""
    creds = get_google_credentials()
    service = build('sheets', 'v4', credentials=creds)

    body = {'values': values}

    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='RAW',
        body=body
    ).execute()

    return result
```

### Notion

```python
# src/tools/notion/client.py
from langchain_core.tools import tool
from notion_client import Client
from src.config.settings import settings

notion = Client(auth=settings.NOTION_API_KEY)

@tool
def query_notion_database(database_id: str, filter_dict: dict = None) -> list:
    """Requête une base de données Notion.

    Args:
        database_id: ID de la base de données
        filter_dict: Filtre optionnel

    Returns:
        Liste des résultats
    """
    query_params = {"database_id": database_id}
    if filter_dict:
        query_params["filter"] = filter_dict

    response = notion.databases.query(**query_params)
    return response.get("results", [])

@tool
def create_notion_page(database_id: str, properties: dict) -> dict:
    """Crée une page dans une base de données Notion.

    Args:
        database_id: ID de la base de données parent
        properties: Propriétés de la page

    Returns:
        Page créée
    """
    response = notion.pages.create(
        parent={"database_id": database_id},
        properties=properties
    )
    return response

@tool
def update_notion_page(page_id: str, properties: dict) -> dict:
    """Met à jour une page Notion."""
    response = notion.pages.update(
        page_id=page_id,
        properties=properties
    )
    return response

@tool
def search_notion(query: str, filter_type: str = None) -> list:
    """Recherche dans Notion.

    Args:
        query: Terme de recherche
        filter_type: "page" ou "database" (optionnel)

    Returns:
        Résultats de recherche
    """
    params = {"query": query}
    if filter_type:
        params["filter"] = {"property": "object", "value": filter_type}

    response = notion.search(**params)
    return response.get("results", [])
```

### Telegram

```python
# src/tools/messaging/telegram.py
from langchain_core.tools import tool
from telegram import Bot
from telegram.constants import ParseMode
from src.config.settings import settings
import asyncio

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

@tool
async def send_telegram_message(
    chat_id: str,
    text: str,
    parse_mode: str = "HTML"
) -> dict:
    """Envoie un message Telegram.

    Args:
        chat_id: ID du chat destination
        text: Texte du message
        parse_mode: HTML ou Markdown

    Returns:
        Informations sur le message envoyé
    """
    message = await bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.HTML if parse_mode == "HTML" else ParseMode.MARKDOWN
    )

    return {
        "message_id": message.message_id,
        "chat_id": message.chat_id,
        "date": message.date.isoformat()
    }

@tool
async def send_telegram_document(
    chat_id: str,
    file_path: str,
    caption: str = None
) -> dict:
    """Envoie un document via Telegram."""
    with open(file_path, 'rb') as doc:
        message = await bot.send_document(
            chat_id=chat_id,
            document=doc,
            caption=caption
        )

    return {
        "message_id": message.message_id,
        "document": message.document.file_id
    }
```

### WhatsApp (Meta Business API)

```python
# src/tools/messaging/whatsapp.py
from langchain_core.tools import tool
import httpx
from src.config.settings import settings

WHATSAPP_API_URL = "https://graph.facebook.com/v18.0"

@tool
async def send_whatsapp_message(
    phone_number: str,
    message: str,
    template_name: str = None
) -> dict:
    """Envoie un message WhatsApp.

    Args:
        phone_number: Numéro au format international (ex: +33612345678)
        message: Texte du message
        template_name: Nom du template (optionnel, pour messages template)

    Returns:
        Réponse de l'API WhatsApp
    """
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    if template_name:
        # Message template
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": "fr"}
            }
        }
    else:
        # Message texte simple
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "text",
            "text": {"body": message}
        }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{WHATSAPP_API_URL}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages",
            headers=headers,
            json=payload
        )
        return response.json()
```

### N8N

```python
# src/tools/integrations/n8n.py
from langchain_core.tools import tool
import httpx
from src.config.settings import settings

@tool
async def trigger_n8n_workflow(
    workflow_id: str,
    payload: dict = None
) -> dict:
    """Déclenche un workflow n8n.

    Args:
        workflow_id: ID du workflow à déclencher
        payload: Données à envoyer au workflow

    Returns:
        Réponse du workflow
    """
    headers = {
        "X-N8N-API-KEY": settings.N8N_API_KEY,
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.N8N_BASE_URL}/webhook/{workflow_id}",
            headers=headers,
            json=payload or {}
        )
        return response.json()

@tool
async def get_n8n_workflow_status(workflow_id: str) -> dict:
    """Obtient le statut d'un workflow n8n."""
    headers = {"X-N8N-API-KEY": settings.N8N_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.N8N_BASE_URL}/api/v1/workflows/{workflow_id}",
            headers=headers
        )
        return response.json()
```

### Cohere Reranker

```python
# src/tools/integrations/reranker.py
from langchain_core.tools import tool
from langchain_cohere import CohereRerank
from langchain.retrievers import ContextualCompressionRetriever
from src.config.settings import settings

@tool
def rerank_documents(
    query: str,
    documents: list[str],
    top_n: int = 5
) -> list[dict]:
    """Reranke des documents avec Cohere.

    Args:
        query: Requête de recherche
        documents: Liste de documents à reranker
        top_n: Nombre de documents à retourner

    Returns:
        Documents rerankés avec scores
    """
    import cohere

    co = cohere.Client(settings.COHERE_API_KEY)

    results = co.rerank(
        model=settings.COHERE_RERANK_MODEL,
        query=query,
        documents=documents,
        top_n=top_n
    )

    return [
        {
            "index": r.index,
            "document": documents[r.index],
            "relevance_score": r.relevance_score
        }
        for r in results.results
    ]


def get_reranking_retriever(base_retriever, top_n: int = 5):
    """Crée un retriever avec reranking Cohere."""
    compressor = CohereRerank(
        cohere_api_key=settings.COHERE_API_KEY,
        model=settings.COHERE_RERANK_MODEL,
        top_n=top_n
    )

    return ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=base_retriever
    )
```

### Slack

```python
# src/tools/messaging/slack.py
from langchain_core.tools import tool
from slack_sdk.web.async_client import AsyncWebClient
from src.config.settings import settings

slack_client = AsyncWebClient(token=settings.SLACK_BOT_TOKEN)

@tool
async def send_slack_message(
    channel: str,
    text: str,
    blocks: list = None
) -> dict:
    """Envoie un message Slack.

    Args:
        channel: ID ou nom du channel
        text: Texte du message
        blocks: Blocks Slack (optionnel)

    Returns:
        Réponse de l'API Slack
    """
    response = await slack_client.chat_postMessage(
        channel=channel,
        text=text,
        blocks=blocks
    )
    return {
        "ok": response["ok"],
        "channel": response["channel"],
        "ts": response["ts"]
    }

@tool
async def upload_slack_file(
    channel: str,
    file_path: str,
    title: str = None,
    initial_comment: str = None
) -> dict:
    """Upload un fichier sur Slack."""
    response = await slack_client.files_upload_v2(
        channel=channel,
        file=file_path,
        title=title,
        initial_comment=initial_comment
    )
    return response.data
```

---

## Gestion des Secrets

### Bonnes Pratiques

1. **Ne jamais commiter de secrets** - Utiliser `.gitignore`
2. **Variables d'environnement** - Toujours via `.env`
3. **Secrets en production** - Utiliser un vault (HashiCorp, AWS Secrets Manager)
4. **Rotation régulière** - Implémenter la rotation des clés API
5. **Principe du moindre privilège** - Scopes minimaux pour chaque service

### Fichier .gitignore

```gitignore
# Environnement
.env
.env.*
!.env.example

# Secrets
secrets/
*.pem
*.key
*credentials*.json
*token*.json
*service_account*.json

# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
*.egg-info/
dist/
build/

# UV - NE PAS IGNORER uv.lock (il doit être commité!)
# Le fichier uv.lock DOIT être versionné pour garantir la reproductibilité

# IDE
.idea/
.vscode/
*.swp
*.swo

# Docker
docker-compose.override.yml

# Logs
*.log
logs/

# Database
*.db
*.sqlite3

# Jupyter
.ipynb_checkpoints/

# OS
.DS_Store
Thumbs.db
```

> **RAPPEL**: Le fichier `uv.lock` ne doit PAS être dans `.gitignore`. Il DOIT être commité pour garantir des builds reproductibles.

---

## GitHub & CI/CD

> **OBLIGATOIRE**: Toutes les opérations GitHub doivent être effectuées via **GitHub CLI (gh)**. Ne pas utiliser l'interface web sauf pour la visualisation.

### Commandes GitHub CLI Essentielles

```bash
# ============================================
# AUTHENTIFICATION
# ============================================

# Se connecter à GitHub
gh auth login

# Vérifier le statut d'authentification
gh auth status

# Se déconnecter
gh auth logout

# ============================================
# GESTION DES REPOSITORIES
# ============================================

# Créer un nouveau repository
gh repo create mon-projet --private --source=. --remote=origin

# Cloner un repository
gh repo clone owner/repo

# Voir les infos du repo courant
gh repo view

# Lister ses repositories
gh repo list

# Forker un repository
gh repo fork owner/repo

# ============================================
# PULL REQUESTS
# ============================================

# Créer une PR
gh pr create --title "Titre de la PR" --body "Description"

# Créer une PR avec template
gh pr create --fill

# Créer une PR draft
gh pr create --draft --title "WIP: Feature X"

# Lister les PRs
gh pr list

# Voir une PR spécifique
gh pr view 123

# Checkout une PR localement
gh pr checkout 123

# Merger une PR
gh pr merge 123 --squash --delete-branch

# Approuver une PR
gh pr review 123 --approve

# Demander des changements
gh pr review 123 --request-changes --body "Corrections nécessaires"

# Ajouter des reviewers
gh pr edit 123 --add-reviewer user1,user2

# ============================================
# ISSUES
# ============================================

# Créer une issue
gh issue create --title "Bug: Description" --body "Détails du bug"

# Lister les issues
gh issue list

# Voir une issue
gh issue view 456

# Fermer une issue
gh issue close 456

# Assigner une issue
gh issue edit 456 --add-assignee @me

# Ajouter des labels
gh issue edit 456 --add-label "bug,priority:high"

# ============================================
# WORKFLOWS (CI/CD)
# ============================================

# Lister les workflows
gh workflow list

# Voir les runs d'un workflow
gh run list --workflow=ci.yml

# Voir le statut d'un run
gh run view 12345

# Voir les logs d'un run
gh run view 12345 --log

# Relancer un workflow échoué
gh run rerun 12345

# Lancer un workflow manuellement
gh workflow run ci.yml

# Lancer avec des inputs
gh workflow run deploy.yml -f environment=production

# Annuler un run en cours
gh run cancel 12345

# Télécharger les artifacts
gh run download 12345

# ============================================
# RELEASES
# ============================================

# Créer une release
gh release create v1.0.0 --title "Version 1.0.0" --notes "Release notes"

# Créer une release avec fichiers
gh release create v1.0.0 ./dist/*.whl --title "Version 1.0.0"

# Créer une release depuis un tag
gh release create v1.0.0 --generate-notes

# Lister les releases
gh release list

# Télécharger une release
gh release download v1.0.0

# Supprimer une release
gh release delete v1.0.0

# ============================================
# GISTS
# ============================================

# Créer un gist
gh gist create fichier.py --public --desc "Description"

# Lister ses gists
gh gist list

# ============================================
# SECRETS (pour GitHub Actions)
# ============================================

# Lister les secrets du repo
gh secret list

# Définir un secret
gh secret set API_KEY --body "valeur_secrete"

# Définir un secret depuis un fichier
gh secret set API_KEY < secret.txt

# Supprimer un secret
gh secret delete API_KEY

# ============================================
# VARIABLES D'ENVIRONNEMENT
# ============================================

# Lister les variables
gh variable list

# Définir une variable
gh variable set ENV_NAME --body "production"

# ============================================
# API GITHUB (pour requêtes avancées)
# ============================================

# Requête GET
gh api repos/{owner}/{repo}/commits

# Requête POST
gh api repos/{owner}/{repo}/issues --method POST -f title="Titre" -f body="Corps"

# Avec pagination
gh api repos/{owner}/{repo}/issues --paginate

# Format JSON
gh api repos/{owner}/{repo} --jq '.stargazers_count'
```

### GitHub Actions Workflow (avec UV)

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: "3.11"
  UV_VERSION: "0.5.0"
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ============================================
  # LINT & TYPE CHECK
  # ============================================
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install UV
        uses: astral-sh/setup-uv@v4
        with:
          version: ${{ env.UV_VERSION }}
          enable-cache: true

      - name: Set up Python
        run: uv python install ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: uv sync --all-extras

      - name: Run Ruff
        run: uv run ruff check src/

      - name: Run MyPy
        run: uv run mypy src/

  # ============================================
  # TESTS
  # ============================================
  test:
    runs-on: ubuntu-latest
    needs: lint

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - name: Install UV
        uses: astral-sh/setup-uv@v4
        with:
          version: ${{ env.UV_VERSION }}
          enable-cache: true

      - name: Set up Python
        run: uv python install ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: uv sync --all-extras

      - name: Run tests
        env:
          DATABASE_URL: postgresql+asyncpg://test_user:test_password@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379/0
        run: uv run pytest --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml

  # ============================================
  # BUILD & PUSH DOCKER
  # ============================================
  build:
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha
            type=ref,event=branch
            type=semver,pattern={{version}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
      - id: detect-private-key
      - id: check-merge-conflict

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.4
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies:
          - pydantic>=2.0
```

---

## Conventions de Code

### Style Python

- **Formateur**: Ruff (compatible Black)
- **Linter**: Ruff
- **Type Checker**: MyPy (mode strict)
- **Docstrings**: Google style
- **Longueur max ligne**: 100 caractères

### Nommage

| Type | Convention | Exemple |
|------|------------|---------|
| Modules | snake_case | `email_sender.py` |
| Classes | PascalCase | `EmailSender` |
| Fonctions | snake_case | `send_email()` |
| Variables | snake_case | `user_email` |
| Constantes | UPPER_SNAKE | `MAX_RETRIES` |
| Types | PascalCase | `EmailPayload` |

### Structure des Imports

```python
# Standard library
import os
import asyncio
from typing import Optional, List

# Third-party
from langchain_core.tools import tool
from pydantic import BaseModel

# Local
from src.config.settings import settings
from src.utils.helpers import format_response
```

### Documentation

```python
async def process_workflow(
    workflow_id: str,
    payload: dict,
    timeout: int = 30
) -> WorkflowResult:
    """Exécute un workflow avec le payload donné.

    Cette fonction charge le workflow depuis la base de données,
    valide le payload, et exécute les étapes séquentiellement.

    Args:
        workflow_id: Identifiant unique du workflow.
        payload: Données d'entrée pour le workflow.
        timeout: Timeout en secondes (défaut: 30).

    Returns:
        WorkflowResult contenant le statut et les données de sortie.

    Raises:
        WorkflowNotFoundError: Si le workflow n'existe pas.
        ValidationError: Si le payload est invalide.
        TimeoutError: Si l'exécution dépasse le timeout.

    Example:
        >>> result = await process_workflow(
        ...     workflow_id="wf_123",
        ...     payload={"email": "user@example.com"}
        ... )
        >>> print(result.status)
        'completed'
    """
    ...
```

---

## Commandes Utiles

### Commandes UV Essentielles

```bash
# ============================================
# GESTION DES DÉPENDANCES
# ============================================

# Initialiser un nouveau projet
uv init

# Synchroniser les dépendances (crée .venv si nécessaire)
uv sync

# Synchroniser avec les dépendances de développement
uv sync --all-extras

# Ajouter une dépendance
uv add langchain

# Ajouter une dépendance de développement
uv add --dev pytest

# Ajouter une dépendance avec version spécifique
uv add "fastapi>=0.115.0"

# Supprimer une dépendance
uv remove langchain

# Mettre à jour toutes les dépendances
uv lock --upgrade

# Mettre à jour une dépendance spécifique
uv lock --upgrade-package langchain

# Voir l'arbre des dépendances
uv tree

# ============================================
# EXÉCUTION DE COMMANDES
# ============================================

# Exécuter un script Python
uv run python src/main.py

# Exécuter avec des arguments
uv run python -m pytest -v

# Exécuter un module
uv run -m uvicorn src.api.app:app --reload

# ============================================
# GESTION PYTHON
# ============================================

# Installer une version spécifique de Python
uv python install 3.11

# Lister les versions Python disponibles
uv python list

# Définir la version Python du projet
uv python pin 3.11
```

### Développement

```bash
# Installer les dépendances (TOUJOURS avec UV)
uv sync --all-extras

# Lancer les services Docker
docker-compose up -d postgres redis

# Lancer l'application (via UV)
uv run uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000

# Exécuter les tests
uv run pytest -v

# Exécuter les tests avec couverture
uv run pytest --cov=src --cov-report=html

# Linter (via UV)
uv run ruff check src/

# Formatter (via UV)
uv run ruff format src/

# Type check (via UV)
uv run mypy src/

# Lancer un script quelconque
uv run python scripts/init_db.py
```

### Base de Données

```bash
# Créer une migration (via UV)
uv run alembic revision --autogenerate -m "Description"

# Appliquer les migrations
uv run alembic upgrade head

# Revenir en arrière
uv run alembic downgrade -1

# Voir l'historique
uv run alembic history
```

### Docker

```bash
# Build l'image
docker build -t langgraph-workflow .

# Lancer avec tous les services
docker-compose up -d

# Voir les logs en temps réel
docker-compose logs -f app

# Entrer dans un container
docker exec -it langgraph-app bash

# Nettoyer
docker-compose down -v
docker system prune -af
```

### Git

```bash
# Créer une branche feature
git checkout -b feature/nom-feature

# Commit conventionnel
git commit -m "feat: ajout de l'intégration Notion"
git commit -m "fix: correction du bug d'authentification"
git commit -m "docs: mise à jour du README"

# Push avec upstream
git push -u origin feature/nom-feature
```

---

## Checklist d'Initialisation d'un Nouveau Projet

Lors de la création d'un nouveau projet à partir de ce boilerplate:

### Outils Prérequis
- [ ] **Installer UV** si pas déjà fait (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- [ ] **Installer GitHub CLI** si pas déjà fait (`brew install gh` ou `winget install GitHub.cli`)
- [ ] **Authentifier gh** avec `gh auth login`

### Configuration du Projet
- [ ] Cloner le repository ou créer un nouveau repo avec `gh repo create`
- [ ] Renommer le projet dans `pyproject.toml`
- [ ] Copier `.env.example` vers `.env`
- [ ] Configurer les clés API nécessaires

### Installation et Setup
- [ ] **Exécuter `uv sync --all-extras`** pour installer les dépendances
- [ ] Lancer `docker-compose up -d`
- [ ] Vérifier la connexion à la DB
- [ ] Créer les migrations initiales avec `uv run alembic upgrade head`
- [ ] Mettre en place les pre-commit hooks avec `uv run pre-commit install`

### GitHub et CI/CD
- [ ] Configurer les secrets GitHub avec `gh secret set`
- [ ] Vérifier que les workflows CI/CD fonctionnent avec `gh run list`
- [ ] Configurer LangSmith (optionnel)

### Développement
- [ ] Adapter la structure des agents/workflows
- [ ] Écrire les premiers tests avec `uv run pytest`
- [ ] Documenter les spécificités du projet

### Finalisation
- [ ] **Commiter le fichier `uv.lock`** (IMPORTANT)
- [ ] Créer la première PR avec `gh pr create` si sur une branche

---

## Notes pour les Agents IA

> **IMPORTANT**: Ce document est ta référence principale. Consulte-le systématiquement avant toute action sur ce projet.

### Règles UV OBLIGATOIRES

> **CRITIQUE**: Ce projet utilise **exclusivement UV** comme gestionnaire de paquets. Les règles suivantes sont NON-NÉGOCIABLES:

1. **JAMAIS utiliser pip, pipenv, poetry ou conda** - Uniquement UV
2. **Pour ajouter une dépendance**: `uv add <package>`
3. **Pour ajouter une dépendance dev**: `uv add --dev <package>`
4. **Pour exécuter un script**: `uv run python script.py`
5. **Pour exécuter un outil**: `uv run pytest`, `uv run ruff`, etc.
6. **Pour synchroniser l'environnement**: `uv sync`
7. **TOUJOURS commiter `uv.lock`** - Ce fichier garantit la reproductibilité
8. **Ne JAMAIS modifier `uv.lock` manuellement** - Il est géré automatiquement

### Règles GitHub CLI (gh) OBLIGATOIRES

> **CRITIQUE**: Toutes les opérations GitHub doivent être effectuées via **gh**. Les règles suivantes sont NON-NÉGOCIABLES:

1. **JAMAIS utiliser l'interface web GitHub** pour les opérations (sauf visualisation)
2. **Pour créer un repo**: `gh repo create`
3. **Pour créer une PR**: `gh pr create`
4. **Pour créer une issue**: `gh issue create`
5. **Pour gérer les workflows**: `gh workflow` et `gh run`
6. **Pour créer une release**: `gh release create`
7. **Pour gérer les secrets**: `gh secret set`
8. **Pour les requêtes API avancées**: `gh api`
9. **TOUJOURS vérifier l'authentification**: `gh auth status`

### Directives Clés

1. **Toujours vérifier** les variables d'environnement requises avant d'ajouter une intégration
2. **Respecter** la structure de fichiers définie
3. **Utiliser** les patterns LangGraph établis (State, Nodes, Edges)
4. **Documenter** tout nouveau tool ou workflow créé
5. **Tester** les intégrations API avant de les utiliser en production
6. **Ne jamais** commiter de secrets ou credentials
7. **Préférer** les opérations asynchrones (async/await)
8. **Logger** les actions importantes pour le debugging
9. **Utiliser `uv run`** pour toute exécution de commande Python

### En Cas de Doute

1. Consulter la documentation officielle LangChain/LangGraph
2. Vérifier les exemples dans `/src/agents/workflows/`
3. S'assurer que les dépendances sont à jour avec `uv tree`
4. Consulter la documentation UV: https://docs.astral.sh/uv/
5. Consulter la documentation GitHub CLI: https://cli.github.com/manual/
6. Pour l'aide sur une commande gh: `gh <command> --help`

---

*Dernière mise à jour: Janvier 2025*
*Version du boilerplate: 1.0.0*
