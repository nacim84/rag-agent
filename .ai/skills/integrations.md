# Intégrations API - Notion, Telegram, WhatsApp, Slack, N8N

## Vue d'ensemble

Ce fichier couvre les intégrations avec les services tiers populaires pour l'automatisation et la communication.

## Notion

### Installation

```bash
uv add notion-client
```

### Configuration

```env
NOTION_API_KEY=secret_...
NOTION_VERSION=2022-06-28
NOTION_DATABASE_ID=...
```

### Tools LangChain

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
    """Met à jour une page Notion.

    Args:
        page_id: ID de la page
        properties: Nouvelles propriétés

    Returns:
        Page mise à jour
    """
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

### Exemples d'Utilisation

```python
# Créer une tâche dans Notion
properties = {
    "Name": {"title": [{"text": {"content": "Nouvelle tâche"}}]},
    "Status": {"select": {"name": "To Do"}},
    "Priority": {"select": {"name": "High"}}
}
page = create_notion_page(database_id="xxx", properties=properties)

# Rechercher des pages
results = search_notion("workflow automation", filter_type="page")
```

## Telegram

### Installation

```bash
uv add python-telegram-bot
```

### Configuration

```env
TELEGRAM_BOT_TOKEN=...
TELEGRAM_WEBHOOK_URL=https://your-domain.com/webhook/telegram
TELEGRAM_CHAT_ID=...
```

### Tools LangChain

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
    """Envoie un document via Telegram.

    Args:
        chat_id: ID du chat
        file_path: Chemin du fichier
        caption: Légende optionnelle

    Returns:
        Informations sur le message
    """
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

@tool
async def send_telegram_photo(
    chat_id: str,
    photo_path: str,
    caption: str = None
) -> dict:
    """Envoie une photo via Telegram."""
    with open(photo_path, 'rb') as photo:
        message = await bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=caption
        )

    return {
        "message_id": message.message_id,
        "photo": message.photo[-1].file_id
    }
```

### Bot Webhook

```python
# src/api/routes/webhooks.py
from fastapi import APIRouter, Request
from telegram import Update
from telegram.ext import Application

router = APIRouter()

@router.post("/telegram")
async def telegram_webhook(request: Request):
    """Handle Telegram webhook."""
    update_dict = await request.json()
    update = Update.de_json(update_dict, bot)

    # Traiter l'update
    # ...

    return {"ok": True}
```

## WhatsApp (Meta Business API)

### Configuration

```env
WHATSAPP_PHONE_NUMBER_ID=...
WHATSAPP_BUSINESS_ACCOUNT_ID=...
WHATSAPP_ACCESS_TOKEN=...
WHATSAPP_VERIFY_TOKEN=...
WHATSAPP_WEBHOOK_URL=https://your-domain.com/webhook/whatsapp
```

### Tools LangChain

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
        template_name: Nom du template (optionnel)

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

@tool
async def send_whatsapp_media(
    phone_number: str,
    media_url: str,
    media_type: str,
    caption: str = None
) -> dict:
    """Envoie un média WhatsApp.

    Args:
        phone_number: Numéro du destinataire
        media_url: URL du média
        media_type: "image", "video", "audio", "document"
        caption: Légende optionnelle

    Returns:
        Réponse de l'API
    """
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": media_type,
        media_type: {
            "link": media_url,
            "caption": caption
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{WHATSAPP_API_URL}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages",
            headers=headers,
            json=payload
        )
        return response.json()
```

## Slack

### Installation

```bash
uv add slack-sdk
```

### Configuration

```env
SLACK_BOT_TOKEN=xoxb-...
SLACK_SIGNING_SECRET=...
SLACK_APP_TOKEN=xapp-...
```

### Tools LangChain

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
    """Upload un fichier sur Slack.

    Args:
        channel: Channel de destination
        file_path: Chemin du fichier
        title: Titre du fichier
        initial_comment: Commentaire initial

    Returns:
        Informations sur le fichier uploadé
    """
    response = await slack_client.files_upload_v2(
        channel=channel,
        file=file_path,
        title=title,
        initial_comment=initial_comment
    )
    return response.data

@tool
async def create_slack_channel(name: str, is_private: bool = False) -> dict:
    """Crée un channel Slack."""
    method = "conversations.create"
    response = await slack_client.api_call(
        method,
        json={
            "name": name,
            "is_private": is_private
        }
    )
    return response.data
```

## N8N

### Configuration

```env
N8N_BASE_URL=http://n8n:5678
N8N_API_KEY=...
N8N_WEBHOOK_URL=...
```

### Tools LangChain

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
    """Obtient le statut d'un workflow n8n.

    Args:
        workflow_id: ID du workflow

    Returns:
        Statut du workflow
    """
    headers = {"X-N8N-API-KEY": settings.N8N_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.N8N_BASE_URL}/api/v1/workflows/{workflow_id}",
            headers=headers
        )
        return response.json()

@tool
async def list_n8n_executions(workflow_id: str, limit: int = 10) -> list:
    """Liste les exécutions récentes d'un workflow."""
    headers = {"X-N8N-API-KEY": settings.N8N_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.N8N_BASE_URL}/api/v1/executions",
            headers=headers,
            params={"workflowId": workflow_id, "limit": limit}
        )
        return response.json()
```

## Cohere (Reranker)

### Installation

```bash
uv add cohere langchain-cohere
```

### Configuration

```env
COHERE_API_KEY=...
COHERE_RERANK_MODEL=rerank-english-v3.0
```

### Tools LangChain

```python
# src/tools/integrations/reranker.py
from langchain_core.tools import tool
from langchain_cohere import CohereRerank
from langchain.retrievers import ContextualCompressionRetriever
from src.config.settings import settings
import cohere

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
    """Crée un retriever avec reranking Cohere.

    Args:
        base_retriever: Retriever de base
        top_n: Nombre de documents à retourner

    Returns:
        Retriever avec reranking
    """
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

## Bonnes Pratiques

### 1. Gestion des Secrets

```python
# ✅ Correct - utiliser settings
from src.config.settings import settings
api_key = settings.NOTION_API_KEY

# ❌ Éviter - hardcoder
api_key = "secret_xxx"
```

### 2. Gestion des Erreurs

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def api_call_with_retry():
    """Appel API avec retry automatique."""
    try:
        response = await client.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        logger.error(f"API call failed: {e}")
        raise
```

### 3. Rate Limiting

```python
from asyncio import Semaphore

# Limiter à 10 requêtes concurrentes
semaphore = Semaphore(10)

async def limited_api_call():
    async with semaphore:
        return await make_api_call()
```

### 4. Logging des Intégrations

```python
import structlog

logger = structlog.get_logger()

@tool
async def send_notification(channel: str, message: str):
    """Envoie une notification avec logging."""
    logger.info(
        "sending_notification",
        channel=channel,
        message_length=len(message)
    )

    try:
        result = await slack_client.chat_postMessage(
            channel=channel,
            text=message
        )
        logger.info("notification_sent", message_id=result["ts"])
        return result
    except Exception as e:
        logger.error("notification_failed", error=str(e))
        raise
```

## Dépendances Requises

```toml
# Notion
notion-client>=2.2.0

# Messaging
python-telegram-bot>=21.0
slack-sdk>=3.27.0

# AI/ML
cohere>=5.0.0
langchain-cohere>=0.3.0

# HTTP
httpx>=0.27.0
aiohttp>=3.9.0
```

## Ressources

- [Notion API](https://developers.notion.com)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)
- [Slack API](https://api.slack.com)
- [N8N](https://docs.n8n.io)
- [Cohere](https://docs.cohere.com)

## Cas d'Usage du Projet

Ces intégrations permettent:

1. **Notion** - Gestion de tâches et documentation automatisée
2. **Telegram/WhatsApp** - Notifications et interactions utilisateur
3. **Slack** - Communication d'équipe et alertes
4. **N8N** - Orchestration de workflows externes
5. **Cohere** - Amélioration de la recherche sémantique
