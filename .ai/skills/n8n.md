# n8n Integration - Guide Technique

## Vue d'ensemble

n8n est une plateforme d'automatisation de workflow "fair-code" qui permet de connecter divers services via une interface visuelle ou du code. Dans ce boilerplate, n8n est utilisé soit comme déclencheur externe, soit comme outil orchestré par nos agents LangGraph.

## Installation (Clients Python)

Pour interagir avec l'API n8n ou gérer des webhooks :

```bash
uv add httpx
```

## Configuration

### Variables d'Environnement

```env
N8N_BASE_URL=https://votre-instance.n8n.cloud
N8N_API_KEY=votre_cle_api_ici
N8N_WEBHOOK_URL=https://votre-instance.n8n.cloud/webhook/
```

## Utilisation de l'API n8n

L'API REST de n8n permet de lister, créer et activer des workflows programmatiquement.

### Lister les Workflows

```python
import httpx
from src.config.settings import settings

async def list_n8n_workflows():
    headers = {"X-N8N-API-KEY": settings.N8N_API_KEY}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.N8N_BASE_URL}/api/v1/workflows",
            headers=headers
        )
        return response.json()
```

## Déclenchement de Workflows via Webhook

C'est la méthode la plus courante pour intégrer LangGraph avec n8n.

### Tool LangChain pour déclencher n8n

```python
# src/tools/integrations/n8n.py
from langchain_core.tools import tool
import httpx
from src.config.settings import settings

@tool
async def trigger_n8n_webhook(
    webhook_id: str,
    payload: dict
) -> dict:
    """Déclenche un workflow n8n via un noeud Webhook.

    Args:
        webhook_id: L'ID ou le slug du webhook n8n
        payload: Les données à envoyer au workflow
    """
    url = f"{settings.N8N_WEBHOOK_URL}{webhook_id}"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()
```

## Intégration LangChain Native dans n8n

n8n possède des noeuds "AI" qui utilisent LangChain. Vous pouvez concevoir une partie de la logique dans n8n et appeler votre boilerplate FastAPI comme un noeud "Tool" ou "HTTP Request".

### Pattern : n8n appelle LangGraph (FastAPI)

1. **n8n** reçoit un événement (ex: Email).
2. **n8n** appelle l'API FastAPI du boilerplate via un noeud **HTTP Request**.
3. **LangGraph** traite la logique complexe (multi-agents).
4. **LangGraph** répond à n8n avec le résultat.
5. **n8n** termine l'automatisation (ex: envoie un Slack).

## Bonnes Pratiques

### 1. Sécurité des Webhooks
Utilisez toujours des headers d'authentification personnalisés ou des tokens de vérification lors de l'appel de vos routes FastAPI depuis n8n.

### 2. Gestion des Erreurs
n8n dispose de noeuds "Error Trigger". Configurez-les pour notifier vos agents LangGraph via un webhook dédié en cas d'échec d'un workflow critique.

### 3. Versioning
Conservez les exports JSON de vos workflows n8n dans le dossier `integrations/n8n/` de ce repository pour permettre le suivi des versions.

## Ressources

- [Documentation API n8n](https://docs.n8n.io/api/v1/)
- [Noeuds LangChain n8n](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.chain-llm/)
- [n8n Expressions](https://docs.n8n.io/code/expressions/)

## Cas d'Usage dans le Projet

1. **Ingestion de données** : n8n surveille une boîte mail et envoie le contenu à LangGraph pour analyse.
2. **Distribution multicanal** : LangGraph génère un rapport, n8n s'occupe de le poster sur Slack, Discord et par Email simultanément.
3. **Human-in-the-loop** : n8n envoie un message avec boutons (Wait for Approval) et renvoie la décision à l'agent LangGraph.
