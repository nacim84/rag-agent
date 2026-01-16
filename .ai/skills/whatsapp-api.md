# WhatsApp Business API - Guide Complet

## Vue d'ensemble

L'API WhatsApp Business (Meta Business) permet d'envoyer et de recevoir des messages WhatsApp de manière programmatique. Cette API est conçue pour les entreprises qui souhaitent communiquer avec leurs clients via WhatsApp.

## Prérequis

### Configuration Meta Business

1. Créer un compte Meta Business: https://business.facebook.com
2. Créer une application WhatsApp Business
3. Configurer un numéro de téléphone WhatsApp Business
4. Obtenir l'accès à l'API

### Variables d'Environnement

```env
WHATSAPP_PHONE_NUMBER_ID=123456789012345
WHATSAPP_BUSINESS_ACCOUNT_ID=123456789012345
WHATSAPP_ACCESS_TOKEN=EAAxxxxxxxxxxxxx
WHATSAPP_VERIFY_TOKEN=my_secure_verify_token
WHATSAPP_WEBHOOK_URL=https://your-domain.com/webhook/whatsapp
WHATSAPP_API_VERSION=v18.0
```

## Configuration de Base

### Client HTTP avec httpx

```python
import httpx
from src.config.settings import settings

WHATSAPP_API_URL = f"https://graph.facebook.com/{settings.WHATSAPP_API_VERSION}"

def get_headers() -> dict:
    """Retourne les headers pour les requêtes WhatsApp API"""
    return {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
```

## Envoyer des Messages

### Messages Texte

```python
import httpx
from src.config.settings import settings

async def send_text_message(phone_number: str, message: str) -> dict:
    """Envoie un message texte WhatsApp.

    Args:
        phone_number: Numéro au format international (ex: +33612345678)
        message: Texte du message

    Returns:
        Réponse de l'API WhatsApp
    """
    url = f"{WHATSAPP_API_URL}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phone_number,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()
```

### Messages Template

Les templates doivent être approuvés par Meta avant utilisation.

```python
async def send_template_message(
    phone_number: str,
    template_name: str,
    language_code: str = "fr",
    parameters: list = None
) -> dict:
    """Envoie un message template WhatsApp.

    Args:
        phone_number: Numéro du destinataire
        template_name: Nom du template approuvé
        language_code: Code de langue (ex: 'fr', 'en')
        parameters: Paramètres du template

    Returns:
        Réponse de l'API
    """
    url = f"{WHATSAPP_API_URL}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {
                "code": language_code
            }
        }
    }

    # Ajouter les paramètres si fournis
    if parameters:
        payload["template"]["components"] = [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": param} for param in parameters
                ]
            }
        ]

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()
```

### Messages avec Boutons Interactifs

```python
async def send_interactive_buttons(
    phone_number: str,
    body_text: str,
    buttons: list[dict]
) -> dict:
    """Envoie un message avec boutons interactifs.

    Args:
        phone_number: Numéro du destinataire
        body_text: Texte principal du message
        buttons: Liste de boutons (max 3)
            [{"id": "btn1", "title": "Option 1"}, ...]

    Returns:
        Réponse de l'API
    """
    url = f"{WHATSAPP_API_URL}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": body_text
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": btn["id"],
                            "title": btn["title"]
                        }
                    }
                    for btn in buttons[:3]  # Max 3 boutons
                ]
            }
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()
```

### Messages avec Liste de Sélection

```python
async def send_interactive_list(
    phone_number: str,
    body_text: str,
    button_text: str,
    sections: list[dict]
) -> dict:
    """Envoie un message avec liste de sélection.

    Args:
        phone_number: Numéro du destinataire
        body_text: Texte principal
        button_text: Texte du bouton pour ouvrir la liste
        sections: Sections avec options
            [{"title": "Section 1", "rows": [{"id": "1", "title": "Option 1"}]}]

    Returns:
        Réponse de l'API
    """
    url = f"{WHATSAPP_API_URL}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {
                "text": body_text
            },
            "action": {
                "button": button_text,
                "sections": sections
            }
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()
```

## Envoyer des Médias

### Images

```python
async def send_image(
    phone_number: str,
    image_url: str,
    caption: str = None
) -> dict:
    """Envoie une image via WhatsApp.

    Args:
        phone_number: Numéro du destinataire
        image_url: URL de l'image (doit être HTTPS)
        caption: Légende optionnelle

    Returns:
        Réponse de l'API
    """
    url = f"{WHATSAPP_API_URL}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "image",
        "image": {
            "link": image_url
        }
    }

    if caption:
        payload["image"]["caption"] = caption

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()
```

### Documents

```python
async def send_document(
    phone_number: str,
    document_url: str,
    filename: str = None,
    caption: str = None
) -> dict:
    """Envoie un document via WhatsApp.

    Args:
        phone_number: Numéro du destinataire
        document_url: URL du document
        filename: Nom du fichier
        caption: Légende optionnelle

    Returns:
        Réponse de l'API
    """
    url = f"{WHATSAPP_API_URL}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "document",
        "document": {
            "link": document_url
        }
    }

    if filename:
        payload["document"]["filename"] = filename

    if caption:
        payload["document"]["caption"] = caption

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()
```

### Vidéos et Audio

```python
async def send_video(
    phone_number: str,
    video_url: str,
    caption: str = None
) -> dict:
    """Envoie une vidéo via WhatsApp."""
    url = f"{WHATSAPP_API_URL}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "video",
        "video": {
            "link": video_url
        }
    }

    if caption:
        payload["video"]["caption"] = caption

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=get_headers(), json=payload)
        response.raise_for_status()
        return response.json()

async def send_audio(
    phone_number: str,
    audio_url: str
) -> dict:
    """Envoie un fichier audio via WhatsApp."""
    url = f"{WHATSAPP_API_URL}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "audio",
        "audio": {
            "link": audio_url
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=get_headers(), json=payload)
        response.raise_for_status()
        return response.json()
```

## Webhooks

### Configuration Webhook (FastAPI)

```python
from fastapi import APIRouter, Request, HTTPException
import hashlib
import hmac

router = APIRouter()

@router.get("/whatsapp")
async def verify_webhook(request: Request):
    """Vérification du webhook par Meta"""
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
        return int(challenge)
    else:
        raise HTTPException(status_code=403, detail="Verification failed")

@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    """Recevoir les messages WhatsApp"""
    # Vérifier la signature (recommandé en production)
    signature = request.headers.get("X-Hub-Signature-256", "")
    body = await request.body()

    # Valider la signature
    expected_signature = "sha256=" + hmac.new(
        settings.WHATSAPP_VERIFY_TOKEN.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=403, detail="Invalid signature")

    # Traiter le webhook
    data = await request.json()

    # Extraire les messages
    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})

            # Messages reçus
            if "messages" in value:
                for message in value["messages"]:
                    await process_incoming_message(message)

            # Statuts de messages
            if "statuses" in value:
                for status in value["statuses"]:
                    await process_message_status(status)

    return {"status": "ok"}
```

### Traitement des Messages Reçus

```python
async def process_incoming_message(message: dict):
    """Traite un message WhatsApp entrant"""
    message_type = message.get("type")
    sender = message.get("from")
    message_id = message.get("id")

    if message_type == "text":
        text = message.get("text", {}).get("body", "")
        print(f"Text from {sender}: {text}")
        # Traiter le texte...

    elif message_type == "image":
        image_id = message.get("image", {}).get("id")
        caption = message.get("image", {}).get("caption", "")
        # Télécharger et traiter l'image...

    elif message_type == "document":
        doc_id = message.get("document", {}).get("id")
        # Télécharger et traiter le document...

    elif message_type == "interactive":
        interactive_type = message.get("interactive", {}).get("type")
        if interactive_type == "button_reply":
            button_id = message["interactive"]["button_reply"]["id"]
            print(f"Button clicked: {button_id}")
        elif interactive_type == "list_reply":
            list_id = message["interactive"]["list_reply"]["id"]
            print(f"List option selected: {list_id}")

async def process_message_status(status: dict):
    """Traite les statuts de messages"""
    message_id = status.get("id")
    status_type = status.get("status")  # sent, delivered, read, failed

    print(f"Message {message_id} status: {status_type}")
```

## Tools LangChain

### Intégration avec LangChain

```python
from langchain_core.tools import tool
import httpx

@tool
async def send_whatsapp_notification(
    phone_number: str,
    message: str
) -> dict:
    """Envoie une notification WhatsApp.

    Args:
        phone_number: Numéro au format international (+33...)
        message: Texte du message

    Returns:
        Résultat de l'envoi
    """
    return await send_text_message(phone_number, message)

@tool
async def send_whatsapp_template(
    phone_number: str,
    template_name: str,
    parameters: list = None
) -> dict:
    """Envoie un message template WhatsApp.

    Args:
        phone_number: Numéro du destinataire
        template_name: Nom du template approuvé
        parameters: Paramètres du template

    Returns:
        Résultat de l'envoi
    """
    return await send_template_message(phone_number, template_name, "fr", parameters)
```

## Bonnes Pratiques

### 1. Gestion des Erreurs

```python
from httpx import HTTPStatusError

async def send_message_safe(phone_number: str, message: str) -> dict:
    """Envoi de message avec gestion d'erreur"""
    try:
        result = await send_text_message(phone_number, message)
        return {"success": True, "result": result}

    except HTTPStatusError as e:
        error_data = e.response.json()
        error_code = error_data.get("error", {}).get("code")

        if error_code == 131026:  # Message undeliverable
            return {"success": False, "error": "Recipient not on WhatsApp"}
        elif error_code == 130429:  # Rate limit
            return {"success": False, "error": "Rate limit exceeded"}
        else:
            return {"success": False, "error": str(e)}

    except Exception as e:
        return {"success": False, "error": str(e)}
```

### 2. Rate Limiting

```python
from asyncio import Semaphore

# Limiter les requêtes concurrentes
whatsapp_semaphore = Semaphore(10)

async def send_with_rate_limit(phone_number: str, message: str):
    async with whatsapp_semaphore:
        return await send_text_message(phone_number, message)
```

### 3. Templates Dynamiques

```python
TEMPLATES = {
    "welcome": {
        "name": "welcome_message",
        "params_count": 1
    },
    "order_confirmation": {
        "name": "order_confirm",
        "params_count": 3
    }
}

async def send_template_by_type(
    phone_number: str,
    template_type: str,
    params: list
):
    """Envoie un template par type"""
    template = TEMPLATES.get(template_type)
    if not template:
        raise ValueError(f"Unknown template type: {template_type}")

    if len(params) != template["params_count"]:
        raise ValueError(f"Expected {template['params_count']} parameters")

    return await send_template_message(
        phone_number,
        template["name"],
        parameters=params
    )
```

## Limites et Quotas

- **Messages par seconde**: 80 (peut varier selon le niveau du compte)
- **Messages template**: Limités selon le niveau de qualité du compte
- **Taille maximale**:
  - Images: 5 MB
  - Vidéos: 16 MB
  - Documents: 100 MB
- **Fenêtre de conversation**: 24h après le dernier message du client

## Ressources

- Documentation officielle: https://developers.facebook.com/docs/whatsapp
- Cloud API: https://developers.facebook.com/docs/whatsapp/cloud-api
- Business Platform: https://business.facebook.com/

## Cas d'Usage du Projet

Dans ce boilerplate, WhatsApp est utilisé pour:

1. Notifications de workflows critiques
2. Alertes en temps réel
3. Envoi de rapports automatisés
4. Communication client bidirectionnelle
5. Confirmation de tâches importantes
6. Support client automatisé
