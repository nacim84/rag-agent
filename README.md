# RAG Agent 🤖

Un agent conversationnel RAG (Retrieval Augmented Generation) multi-tenant, conçu pour interroger des documents métiers via une architecture robuste basée sur LangGraph, FastAPI et PostgreSQL (PGVector).

## 🎯 Objectifs

- **RAG Multi-domaine** : Routage intelligent entre Comptabilité, Transaction et Exploitation.
- **Multi-tenant** : Isolation stricte des données par client (`documents_{domain}_{client}`).
- **Mémoire Persistante** : Conservation du contexte de conversation entre les sessions.
- **Sources Multiples** : Ingestion via API (PDF, TXT) et connecteurs Google Drive.

## 🛠 Stack Technologique

| Composant | Technologie | Rôle |
|-----------|-------------|------|
| **Langage** | Python 3.11 | Cœur du système |
| **Orchestration** | LangGraph | State Machine et flux de l'agent |
| **API** | FastAPI | Interface HTTP REST |
| **Base de Données** | PostgreSQL 16 | Stockage vectoriel (PGVector) et relationnel |
| **LLM** | Google Gemini | Génération de texte et Embeddings |
| **Reranker** | Cohere | Ré-ordonnancement pour pertinence accrue |
| **Task Queue** | Celery + Redis | Traitements asynchrones (Worker) |
| **Package Manager** | UV (Astral) | Gestionnaire de dépendances ultra-rapide |
| **Infra** | Docker Compose | Déploiement conteneurisé |

## 📋 Prérequis

- **Docker** & **Docker Compose**
- **Clés API** :
  - `GOOGLE_API_KEY` (Gemini)
  - `COHERE_API_KEY` (Rerank)
  - *(Optionnel)* Credentials Google Service Account (pour Drive)

## 🚀 Installation & Démarrage

### 1. Configuration
Copiez le fichier d'exemple et remplissez vos clés API :
```bash
cp .env.example .env
# Éditez .env avec vos clés
```

### 2. Lancement (Docker)
L'application est prête pour la production via Docker Compose :
```bash
docker-compose up -d --build
```

L'API sera accessible sur : `http://localhost:8000`

### 3. Vérification
```bash
curl http://localhost:8000/health
# {"status":"ok","app_name":"rag-agent"}
```

## 💡 Exemples d'Usage

Authentification par header : `X-API-Key: sk_votreClientId_secret` (Le client ID est extrait automatiquement).

### 1. Ingérer un document (PDF)
```bash
curl -X POST "http://localhost:8000/api/v1/ingest" \
  -H "X-API-Key: sk_clientA_123" \
  -F "file=@./facture.pdf" \
  -F "domain=comptable"
```

### 2. Discuter avec les documents (Chat)
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_clientA_123" \
  -d 
  '{'
    "query": "Quel est le montant total de la facture ?",
    "session_id": "session_1"
  '}'
```

## 📂 Structure du Projet

```
rag-agent/
├── .ai/                    # Mémoire du projet et documentation technique
├── src/
│   ├── agents/workflows/   # Définitions des graphes LangGraph (rag_workflow.py)
│   ├── api/routes/         # Endpoints API (chat, ingest)
│   ├── config/             # Configuration (Settings, Database, Logging)
│   ├── graphs/             # Nœuds et États du graphe (nodes.py, state.py)
│   ├── rag/                # Logique RAG (Embeddings, Retriever)
│   └── tools/              # Outils externes (Google Drive)
├── scripts/                # Scripts utilitaires et de test
├── tests/                  # Tests unitaires et d'intégration
├── docker-compose.yml      # Orchestration
└── pyproject.toml          # Dépendances (UV)
```

## 📏 Conventions de Code

- **Gestionnaire de paquets** : Utiliser exclusivement `uv`.
  - `uv sync` : Installer les dépendances.
  - `uv add <package>` : Ajouter un paquet.
- **Style** : Ruff est utilisé pour le linting et le formatage.
- **Tests** : Pytest pour les tests unitaires et d'intégration.
  - `uv run pytest` : Lancer les tests.

## 🛡️ Sécurité

- Les clés API doivent être dans le fichier `.env` (jamais commité).
- L'API utilise une validation basique de clé API via header `X-API-Key`.
- L'isolation multi-tenant est garantie par le nommage des tables vectorielles.

---
*Généré par Gemini Agent - Janvier 2026*