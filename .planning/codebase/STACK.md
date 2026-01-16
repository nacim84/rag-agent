# Technology Stack

**Analysis Date:** 2026-01-16

## Languages

**Primary:**
- Python 3.11 - Core application language (all source code in `src/`)

**Secondary:**
- SQL - Database initialization scripts (`scripts/init_db.sql`)
- JSON - N8N workflow configurations (`n8n_assets/`)

## Runtime

**Environment:**
- Python 3.11 (pinned in `.python-version`)
- Docker containers (production and development)

**Package Manager:**
- UV (Astral) - Modern Python package manager
- Lockfile: `uv.lock` present (894KB)

## Frameworks

**Core:**
- LangGraph >=0.2.0 - Agent workflow orchestration
- LangChain >=0.3.0 - LLM abstraction layer
- FastAPI >=0.115.0 - REST API framework

**Testing:**
- pytest >=8.0.0 - Test runner
- pytest-asyncio >=0.23.0 - Async test support
- pytest-cov >=4.1.0 - Coverage reporting
- pytest-mock >=3.12.0 - Mocking utilities

**Build/Dev:**
- Ruff >=0.4.0 - Linting and formatting
- mypy >=1.10.0 - Static type checking
- pre-commit >=3.7.0 - Git hooks
- Alembic >=1.13.0 - Database migrations

## Key Dependencies

**LLM Providers:**
- langchain-openai >=0.2.0 - OpenAI GPT models
- langchain-anthropic >=0.2.0 - Anthropic Claude models
- langchain-google-genai >=2.0.0 - Google Gemini models
- langchain-cohere >=0.3.0 - Cohere models and reranking

**Database/ORM:**
- SQLAlchemy[asyncio] >=2.0.0 - Async ORM
- psycopg[binary] >=3.1.0 - PostgreSQL driver (sync)
- asyncpg >=0.29.0 - PostgreSQL async driver
- langgraph-checkpoint-postgres >=0.1.0 - LangGraph state persistence

**Task Queue:**
- Celery >=5.3.0 - Distributed task processing
- Redis >=5.0.0 - Message broker and caching

**HTTP/Networking:**
- httpx >=0.27.0 - Modern async HTTP client
- aiohttp >=3.9.0 - Async HTTP client/server
- uvicorn[standard] >=0.30.0 - ASGI server

**Validation/Config:**
- Pydantic >=2.0.0 - Data validation
- pydantic-settings >=2.0.0 - Settings management
- python-dotenv >=1.0.0 - Environment loading

**Observability:**
- LangSmith >=0.1.0 - LLM tracing and debugging
- structlog >=24.0.0 - Structured logging
- tenacity >=8.2.0 - Retry logic

**External Service SDKs:**
- google-api-python-client >=2.100.0 - Google APIs
- notion-client >=2.2.0 - Notion API
- python-telegram-bot >=21.0 - Telegram bots
- slack-sdk >=3.27.0 - Slack integration
- cohere >=5.0.0 - Cohere API
- tweepy >=4.14.0 - Twitter/X API

## Configuration

**Environment:**
- `.env` file loaded via pydantic-settings
- Settings class in `src/config/settings.py`
- LRU-cached singleton pattern for settings access

**Required Environment Variables:**
- `DATABASE_URL` - PostgreSQL connection string (asyncpg format)
- `REDIS_URL` - Redis connection for caching
- At least one LLM provider key (OPENAI_API_KEY, ANTHROPIC_API_KEY, or GOOGLE_API_KEY)

**Build Configuration:**
- `pyproject.toml` - Project metadata and dependencies
- `uv.lock` - Locked dependency versions
- `Dockerfile` - Multi-stage production build
- `Dockerfile.dev` - Development build

## Container Configuration

**Docker Compose Services:**
- `app` - Main FastAPI application (port 8000)
- `worker` - Celery worker (4 concurrent tasks)
- `beat` - Celery scheduler
- `postgres` - PostgreSQL 16 Alpine
- `redis` - Redis 7 Alpine
- `pgadmin` - Database admin UI (dev profile, port 5050)
- `n8n` - Workflow automation (automation profile, port 5678)
- `qdrant` - Vector database (vectordb profile, ports 6333/6334)

**Docker Build:**
- Multi-stage build using UV for dependency installation
- Base image: `python:3.11-slim`
- UV installed from `ghcr.io/astral-sh/uv:latest`
- Virtual environment at `/app/.venv`

## Platform Requirements

**Development:**
- Python 3.11+
- UV package manager
- Docker and Docker Compose
- PostgreSQL client (optional, for local development)

**Production:**
- Docker runtime
- PostgreSQL 16 database
- Redis 7 server
- Minimum 4 worker processes recommended

## Code Quality Tools

**Ruff Configuration:**
- Target: Python 3.11
- Line length: 100
- Rules: E, F, I, N, W, UP, B, C4, SIM
- Ignored: E501 (line too long - handled by formatter)

**MyPy Configuration:**
- Strict mode enabled
- Missing imports ignored

**Pytest Configuration:**
- Async mode: auto
- Test paths: `tests/`

---

*Stack analysis: 2026-01-16*
