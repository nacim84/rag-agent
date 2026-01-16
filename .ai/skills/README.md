# Skills - Documentation Technique du Projet

## Vue d'ensemble

Ce dossier contient la documentation technique et les bonnes pratiques pour toutes les technologies utilisées dans le projet LangGraph Workflows Boilerplate.

## Index des Compétences

### Technologies Core

1. **[LangChain](./langchain.md)** - Framework pour applications LLM
   - Agents, Chaînes, Outils, Prompts
   - Intégration multi-LLM (OpenAI, Anthropic, Google)
   - Observabilité avec LangSmith

2. **[LangGraph](./langgraph.md)** - Orchestration de workflows stateful
   - StateGraph, Nodes, Edges
   - Checkpointing et persistence
   - Patterns multi-agents

3. **[Cohere](./cohere-api.md)** - Services d'IA avancés
   - Reranking pour RAG, Embeddings
   - Chat models (Command R+), Classification
   - Optimisation de recherche sémantique

4. **[FastAPI](./fastapi.md)** - Framework API moderne
   - Routes async, validation, dependency injection
   - Middleware, CORS, WebSockets
   - Documentation automatique

5. **[Pydantic](./pydantic.md)** - Validation de données
   - BaseModel, validators, settings
   - Sérialisation/désérialisation
   - Types avancés

### Infrastructure

6. **[UV](./uv.md)** - Gestionnaire de paquets Python (**OBLIGATOIRE**)
   - Installation, gestion des dépendances
   - Commandes essentielles
   - Docker et CI/CD

7. **[PostgreSQL & SQLAlchemy](./postgresql-sqlalchemy.md)** - Base de données
   - Modèles async ORM
   - Queries, transactions, relations
   - Repository pattern

8. **[Docker](./docker.md)** - Containerisation
   - Dockerfile multi-stage avec UV
   - Docker Compose pour orchestration
   - Bonnes pratiques

### Intégrations

9. **[Google Workspace APIs](./google-apis.md)** - Drive, Gmail, Sheets
   - OAuth2 et Service Accounts
   - Tools LangChain pour chaque service
   - Exemples d'utilisation

10. **[Notion](./notion-api.md)** - Gestion de base de connaissances
    - Bases de données, pages, blocs
    - Automatisation de documentation
    - Intégration LangChain

11. **[Telegram](./telegram-api.md)** - Interface de communication Bot
    - Webhooks, Commands, Inline Keyboards
    - Notifications et interaction asynchrone

12. **[WhatsApp](./whatsapp-api.md)** - Meta Business API
    - Templates, messages interactifs, médias
    - Webhooks et validation de signature

13. **[Autres Intégrations](./integrations.md)** - Slack et Patterns
    - Configuration Slack et outils
    - Bonnes pratiques générales d'intégration

14. **[n8n](./n8n.md)** - Automatisation et Orchestration Externe
    - Déclenchement par Webhooks
    - Interaction API n8n
    - Intégration hybride LangChain/n8n

## Comment Utiliser ces Fichiers

### Pour les Développeurs

1. **Avant de commencer** - Lire UV.md pour configurer l'environnement
2. **Pour une feature** - Consulter les fichiers pertinents (ex: LangGraph pour workflows)
3. **Pour une intégration** - Voir les guides spécifiques (Notion, Telegram, n8n, etc.)
4. **Pour le déploiement** - Lire Docker.md

### Pour les Agents IA

Ces fichiers servent de **mémoire de compétences** pour les agents IA travaillant sur ce projet. Ils contiennent:

- ✅ Exemples de code fonctionnels
- ✅ Patterns recommandés
- ✅ Bonnes pratiques
- ✅ Configurations types
- ✅ Commandes courantes

## Structure Recommandée

```
ai/
├── skills/
│   ├── README.md                        # Ce fichier
│   ├── langchain.md                     # LangChain
│   ├── langgraph.md                     # LangGraph
│   ├── cohere-api.md                    # Cohere AI
│   ├── fastapi.md                       # FastAPI
│   ├── pydantic.md                      # Pydantic
│   ├── uv.md                           # UV (gestionnaire)
│   ├── postgresql-sqlalchemy.md        # Base de données
│   ├── docker.md                       # Containerisation
│   ├── google-apis.md                  # Google Workspace
│   ├── notion-api.md                   # Notion
│   ├── telegram-api.md                 # Telegram
│   ├── whatsapp-api.md                 # WhatsApp
│   ├── n8n.md                          # n8n Automation
│   └── integrations.md                 # Autres (Slack)
```

## Règles Importantes

### 1. UV est OBLIGATOIRE

> **CRITIQUE**: Toutes les opérations Python DOIVENT passer par UV

```bash
# ✅ Correct
uv add package
uv run python script.py
uv run pytest

# ❌ JAMAIS faire cela
pip install package
python script.py
pytest
```

### 2. Async par Défaut

> Toutes les fonctions I/O doivent être async

```python
# ✅ Correct
async def get_data():
    async with session.get(url) as response:
        return await response.json()

# ❌ Éviter
def get_data():
    response = requests.get(url)
    return response.json()
```

### 3. Type Hints Obligatoires

> Utiliser les annotations de type partout

```python
# ✅ Correct
async def process_workflow(
    workflow_id: str,
    payload: dict
) -> WorkflowResult:
    ...

# ❌ Éviter
async def process_workflow(workflow_id, payload):
    ...
```

### 4. Pydantic pour Validation

> Toujours valider les données avec Pydantic

```python
# ✅ Correct
class WorkflowInput(BaseModel):
    workflow_id: str
    payload: dict

# ❌ Éviter
def process(data):
    workflow_id = data['workflow_id']
    ...
```

## Conventions de Code

### Nommage

| Type | Convention | Exemple |
|------|------------|---------|
| Modules | snake_case | `email_sender.py` |
| Classes | PascalCase | `EmailSender` |
| Fonctions | snake_case | `send_email()` |
| Variables | snake_case | `user_email` |
| Constantes | UPPER_SNAKE | `MAX_RETRIES` |

### Imports

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

### Docstrings (Google Style)

```python
async def execute_workflow(workflow_id: str, timeout: int = 30) -> dict:
    """Execute a workflow with the given configuration.

    Args:
        workflow_id: Unique identifier for the workflow.
        timeout: Maximum execution time in seconds.

    Returns:
        Dictionary containing execution results.

    Raises:
        WorkflowNotFoundError: If workflow doesn't exist.
        TimeoutError: If execution exceeds timeout.

    Example:
        >>> result = await execute_workflow("wf_123", timeout=60)
        >>> print(result['status'])
        'completed'
    """
    pass
```

## Stack Complet

### Core
- Python 3.11+
- UV (gestionnaire de paquets)
- LangChain & LangGraph
- Cohere (Reranking & Chat)
- FastAPI & Uvicorn
- Pydantic

### Base de Données
- PostgreSQL 15+
- SQLAlchemy (async)
- Alembic (migrations)

### Cache & Queue
- Redis
- Celery

### Intégrations
- OpenAI, Anthropic, Google AI, Cohere
- Google Workspace (Drive, Gmail, Sheets)
- Notion, Telegram, WhatsApp, Slack
- N8N, Zapier

### DevOps
- Docker & Docker Compose
- GitHub Actions
- GitHub CLI (gh)

## Ressources Externes

### Documentation Officielle

- [LangChain](https://docs.langchain.com)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [Cohere](https://docs.cohere.com)
- [FastAPI](https://fastapi.tiangolo.com)
- [Pydantic](https://docs.pydantic.dev)
- [UV](https://docs.astral.sh/uv/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)

### Communautés

- [LangChain Discord](https://discord.gg/langchain)
- [FastAPI Discord](https://discord.gg/fastapi)

## Maintenance

Ces fichiers doivent être mis à jour lors de:

- Ajout d'une nouvelle technologie
- Changement de version majeure
- Découverte de nouvelles bonnes pratiques
- Ajout de patterns utiles

## Contribution

Pour ajouter ou modifier des compétences:

1. Créer un nouveau fichier `.md` dans ce dossier
2. Suivre le format des fichiers existants
3. Ajouter au README.md
4. Commiter avec un message descriptif

---

**Version**: 1.1.0
**Dernière mise à jour**: Janvier 2026
