# UV - Gestionnaire de Paquets Python

## Vue d'ensemble

UV est un gestionnaire de paquets Python ultra-rapide écrit en Rust par Astral (créateurs de Ruff). Il remplace pip, pipenv, poetry et conda. **C'est l'outil OBLIGATOIRE pour ce projet.**

## Installation

```bash
# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Vérifier l'installation
uv --version
```

## Commandes Essentielles

### Initialisation de Projet

```bash
# Initialiser un nouveau projet
uv init

# Initialiser avec Python spécifique
uv init --python 3.11
```

### Gestion des Dépendances

```bash
# Synchroniser les dépendances (crée .venv si nécessaire)
uv sync

# Synchroniser avec les dépendances de développement
uv sync --all-extras

# Ajouter une dépendance
uv add langchain

# Ajouter une dépendance de développement
uv add --dev pytest

# Ajouter avec version spécifique
uv add "fastapi>=0.115.0"

# Supprimer une dépendance
uv remove langchain

# Mettre à jour toutes les dépendances
uv lock --upgrade

# Mettre à jour une dépendance spécifique
uv lock --upgrade-package langchain

# Voir l'arbre des dépendances
uv tree
```

### Exécution de Commandes

```bash
# Exécuter un script Python
uv run python src/main.py

# Exécuter avec des arguments
uv run python -m pytest -v

# Exécuter un module
uv run -m uvicorn src.api.app:app --reload

# Exécuter une commande installée
uv run pytest
uv run ruff check src/
uv run mypy src/
```

### Gestion de Python

```bash
# Installer une version spécifique de Python
uv python install 3.11

# Lister les versions Python disponibles
uv python list

# Définir la version Python du projet
uv python pin 3.11
```

## Configuration pyproject.toml

```toml
[project]
name = "langgraph-workflow"
version = "0.1.0"
description = "Boilerplate pour workflows agentiques LangGraph"
requires-python = ">=3.11"
dependencies = [
    "langchain>=0.3.0",
    "langgraph>=0.2.0",
    "fastapi>=0.115.0",
    # ... autres dépendances
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "ruff>=0.4.0",
    "mypy>=1.10.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=8.0.0",
    "ruff>=0.4.0",
]

[tool.uv.sources]
# Sources personnalisées si nécessaire
# langchain = { git = "https://github.com/langchain-ai/langchain.git" }
```

## Fichier .python-version

```
3.11
```

Ce fichier indique à UV quelle version de Python utiliser. UV peut automatiquement télécharger et gérer cette version.

## Workflow de Développement

### 1. Nouveau Projet

```bash
# Cloner le repo
git clone <repository-url>
cd langgraph-workflows-boilerplate

# Créer l'environnement et installer les dépendances
uv sync --all-extras

# Lancer l'application
uv run uvicorn src.api.app:app --reload
```

### 2. Ajouter une Nouvelle Dépendance

```bash
# Ajouter la dépendance
uv add requests

# UV met automatiquement à jour pyproject.toml et uv.lock
# Commiter les deux fichiers
git add pyproject.toml uv.lock
git commit -m "feat: add requests dependency"
```

### 3. Exécuter des Tests

```bash
# Exécuter tous les tests
uv run pytest

# Avec couverture
uv run pytest --cov=src --cov-report=html

# Tests spécifiques
uv run pytest tests/test_workflows.py -v
```

### 4. Linting et Formatting

```bash
# Linter
uv run ruff check src/

# Auto-fix
uv run ruff check src/ --fix

# Formatter
uv run ruff format src/

# Type checking
uv run mypy src/
```

### 5. Migrations de Base de Données

```bash
# Créer une migration
uv run alembic revision --autogenerate -m "Add new table"

# Appliquer les migrations
uv run alembic upgrade head

# Revenir en arrière
uv run alembic downgrade -1
```

## Avantages de UV

### 1. Performance

- **10-100x plus rapide** que pip
- Installation parallèle des dépendances
- Cache global intelligent

### 2. Lockfile

- `uv.lock` garantit des builds reproductibles
- **TOUJOURS commiter uv.lock**
- Équivalent à poetry.lock ou Pipfile.lock

### 3. Gestion Python Intégrée

- Pas besoin de pyenv
- UV télécharge et gère les versions Python
- Support multi-versions

### 4. Compatibilité

- Compatible avec pip, requirements.txt
- Support complet de PEP standards
- Migration facile depuis pip/poetry/pipenv

## Docker avec UV

### Dockerfile Multi-Stage

```dockerfile
# STAGE 1: Builder
FROM python:3.11-slim AS builder

# Installer UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

# Copier les fichiers de dépendances
COPY pyproject.toml uv.lock ./

# Installer les dépendances
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copier le code source
COPY . .

# Installer le projet
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# STAGE 2: Runtime
FROM python:3.11-slim AS runtime

ENV PYTHONPATH=/app/src \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Copier l'environnement virtuel
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## GitHub Actions avec UV

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install UV
        uses: astral-sh/setup-uv@v4
        with:
          version: "0.5.0"
          enable-cache: true

      - name: Set up Python
        run: uv python install 3.11

      - name: Install dependencies
        run: uv sync --all-extras

      - name: Run tests
        run: uv run pytest --cov=src
```

## Bonnes Pratiques

### 1. TOUJOURS Utiliser UV

- **JAMAIS** utiliser pip, pipenv, poetry directement
- Toutes les commandes Python via `uv run`
- Toutes les installations via `uv add`

### 2. Commiter uv.lock

```gitignore
# .gitignore
.venv/
__pycache__/

# NE PAS IGNORER uv.lock !
# uv.lock DOIT être commité
```

### 3. Utiliser uv run

```bash
# ✅ Correct
uv run python script.py
uv run pytest
uv run uvicorn app:app

# ❌ Incorrect
python script.py
pytest
uvicorn app:app
```

### 4. Scripts dans pyproject.toml

```toml
[project.scripts]
start = "uvicorn src.api.app:app"
dev = "uvicorn src.api.app:app --reload"
test = "pytest"

# Utilisation
uv run start
uv run dev
uv run test
```

## Dépannage

### Cache Problématique

```bash
# Nettoyer le cache
uv cache clean

# Forcer la réinstallation
uv sync --reinstall
```

### Problèmes de Lock

```bash
# Régénérer le lockfile
uv lock --upgrade

# Synchroniser avec le lockfile exact
uv sync --frozen
```

### Conflits de Dépendances

```bash
# Voir les détails
uv tree

# Forcer une version spécifique
uv add "package==1.0.0"
```

## Ressources

- Documentation officielle: https://docs.astral.sh/uv/
- GitHub: https://github.com/astral-sh/uv
- Migration depuis pip: https://docs.astral.sh/uv/pip/

## Règles OBLIGATOIRES pour ce Projet

> **CRITIQUE**: Ces règles sont NON-NÉGOCIABLES

1. **JAMAIS** utiliser pip, pipenv, poetry ou conda
2. **TOUJOURS** utiliser `uv add` pour ajouter des dépendances
3. **TOUJOURS** utiliser `uv run` pour exécuter des commandes
4. **TOUJOURS** commiter `uv.lock`
5. **JAMAIS** modifier `uv.lock` manuellement
6. **TOUJOURS** utiliser `uv sync` après pull
7. **TOUJOURS** tester avec `uv run pytest` avant commit
