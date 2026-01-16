# LangGraph Workflows Boilerplate

Ce projet est un boilerplate pour créer des workflows agentiques avec LangChain et LangGraph.

## Installation

1.  Installer UV:
    ```bash
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

2.  Installer les dépendances:
    ```bash
    uv sync
    ```

3.  Configurer l'environnement:
    Copiez `.env.example` vers `.env` et remplissez les variables.

4.  Lancer l'application:
    ```bash
    uv run uvicorn src.api.app:app --reload
    ```
