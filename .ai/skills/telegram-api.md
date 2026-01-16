# Telegram Bot API - Guide Complet

## Vue d'ensemble

La Telegram Bot API permet de créer des bots interactifs pour Telegram. La bibliothèque `python-telegram-bot` est un wrapper Python moderne et asynchrone pour cette API.

## Installation

```bash
uv add python-telegram-bot
```

## Configuration

### Variables d'Environnement

```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_WEBHOOK_URL=https://your-domain.com/webhook/telegram
TELEGRAM_CHAT_ID=123456789
```

### Obtenir un Token Bot

1. Ouvrir Telegram et chercher **@BotFather**
2. Envoyer `/newbot` et suivre les instructions
3. Récupérer le token fourni par BotFather
4. Configurer les paramètres du bot (description, photo de profil, etc.)

## Concepts de Base

### Application et Handlers

```python
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Créer l'application
application = Application.builder().token("YOUR_BOT_TOKEN").build()

# Ajouter des handlers
application.add_handler(CommandHandler("start", start_callback))
application.add_handler(MessageHandler(filters.TEXT, text_callback))

# Lancer le bot en polling
application.run_polling(allowed_updates=Update.ALL_TYPES)
```

## Commandes de Base

### Command Handlers

```python
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler pour /start"""
    await update.message.reply_text("Welcome to my awesome bot!")

async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler pour /help"""
    help_text = """
    Available commands:
    /start - Start the bot
    /help - Show this help message
    /info - Get information
    """
    await update.message.reply_text(help_text)

async def info_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler pour /info avec arguments"""
    # Récupérer les arguments de la commande
    args = context.args
    if args:
        await update.message.reply_text(f"Info about: {' '.join(args)}")
    else:
        await update.message.reply_text("Please provide arguments: /info <topic>")

# Ajouter les handlers
application.add_handler(CommandHandler("start", start_callback))
application.add_handler(CommandHandler("help", help_callback))
application.add_handler(CommandHandler("info", info_callback))
```

## Messages et Médias

### Envoyer des Messages

```python
async def send_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exemples d'envoi de différents types de messages"""

    # Message texte simple
    await update.message.reply_text("Hello!")

    # Message avec formatting (Markdown)
    await update.message.reply_text(
        "*Bold* _Italic_ `Code` [Link](https://example.com)",
        parse_mode="Markdown"
    )

    # Message avec formatting (HTML)
    await update.message.reply_text(
        "<b>Bold</b> <i>Italic</i> <code>Code</code>",
        parse_mode="HTML"
    )

    # Répondre à un message spécifique
    await update.message.reply_text(
        "This is a reply",
        reply_to_message_id=update.message.message_id
    )
```

### Envoyer des Photos et Documents

```python
async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envoyer une photo"""
    await update.message.reply_photo(
        photo=open('image.jpg', 'rb'),
        caption="Here's your image!"
    )

    # Ou avec une URL
    await update.message.reply_photo(
        photo="https://example.com/image.jpg",
        caption="Image from URL"
    )

async def send_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envoyer un document"""
    await update.message.reply_document(
        document=open('document.pdf', 'rb'),
        filename="report.pdf",
        caption="Your PDF document"
    )

async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envoyer une vidéo"""
    await update.message.reply_video(
        video=open('video.mp4', 'rb'),
        caption="Video file",
        supports_streaming=True
    )

async def send_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envoyer un fichier audio"""
    await update.message.reply_audio(
        audio=open('audio.mp3', 'rb'),
        title="Song Title",
        performer="Artist Name"
    )
```

### Recevoir et Télécharger des Fichiers

```python
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Recevoir et télécharger une photo"""
    # Récupérer la photo en plus haute résolution
    photo = update.message.photo[-1]

    # Télécharger le fichier
    photo_file = await photo.get_file()
    await photo_file.download_to_drive(f"downloaded_{photo_file.file_id}.jpg")

    await update.message.reply_text(f"Photo saved! File ID: {photo.file_id}")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Recevoir et télécharger un document"""
    document = update.message.document

    # Vérifier la taille du fichier
    if document.file_size > 20 * 1024 * 1024:  # 20 MB
        await update.message.reply_text("File too large!")
        return

    # Télécharger le document
    doc_file = await document.get_file()
    await doc_file.download_to_drive(f"downloaded_{document.file_name}")

    await update.message.reply_text(f"Document saved: {document.file_name}")

# Ajouter les handlers
application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
```

## Inline Keyboards (Boutons Interactifs)

### Créer des Inline Keyboards

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envoyer un message avec clavier inline"""
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [InlineKeyboardButton("Option 3", callback_data="3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please choose:", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler pour les boutons callback"""
    query = update.callback_query

    # IMPORTANT: Toujours répondre aux callback queries
    await query.answer()

    # Éditer le message original
    await query.edit_message_text(text=f"Selected option: {query.data}")

    # Ou envoyer un nouveau message
    # await query.message.reply_text(f"You selected: {query.data}")

# Ajouter les handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_callback))
```

### Keyboard Dynamique avec Confirmation

```python
async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Menu avec plusieurs niveaux"""
    keyboard = [
        [InlineKeyboardButton("View Profile", callback_data="profile")],
        [InlineKeyboardButton("Settings", callback_data="settings")],
        [InlineKeyboardButton("Help", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Main Menu:", reply_markup=reply_markup)

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler pour le menu"""
    query = update.callback_query
    await query.answer()

    if query.data == "profile":
        await query.edit_message_text("👤 Your Profile\nName: John Doe")

    elif query.data == "settings":
        # Sous-menu
        keyboard = [
            [InlineKeyboardButton("Notifications", callback_data="notif")],
            [InlineKeyboardButton("Privacy", callback_data="privacy")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("⚙️ Settings:", reply_markup=reply_markup)

    elif query.data == "help":
        await query.edit_message_text("❓ Help information...")

    elif query.data == "back":
        # Retour au menu principal
        await show_menu(query, context)

application.add_handler(CommandHandler("menu", show_menu))
application.add_handler(CallbackQueryHandler(handle_menu))
```

## Message Handlers

### Filtres de Messages

```python
from telegram.ext import MessageHandler, filters

# Texte uniquement
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

# Photos
application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

# Documents
application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

# Vidéos
application.add_handler(MessageHandler(filters.VIDEO, handle_video))

# Audio
application.add_handler(MessageHandler(filters.AUDIO, handle_audio))

# Messages vocaux
application.add_handler(MessageHandler(filters.VOICE, handle_voice))

# Localisation
application.add_handler(MessageHandler(filters.LOCATION, handle_location))

# Contact
application.add_handler(MessageHandler(filters.CONTACT, handle_contact))

# Messages d'un utilisateur spécifique
application.add_handler(MessageHandler(filters.User(user_id=123456), handle_specific_user))

# Messages d'un chat spécifique
application.add_handler(MessageHandler(filters.Chat(chat_id=-123456), handle_group))

# Combinaison de filtres
application.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex(r"^\d+$"),  # Messages contenant seulement des chiffres
        handle_numbers
    )
)
```

## Context et Persistence

### Utiliser context.user_data et context.chat_data

```python
async def set_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stocker des données utilisateur"""
    name = " ".join(context.args)
    context.user_data['name'] = name
    await update.message.reply_text(f"Name saved: {name}")

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Récupérer des données utilisateur"""
    name = context.user_data.get('name', 'Unknown')
    await update.message.reply_text(f"Your name is: {name}")

async def increment_counter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Compteur par chat"""
    count = context.chat_data.get('counter', 0)
    count += 1
    context.chat_data['counter'] = count
    await update.message.reply_text(f"Chat counter: {count}")
```

### Persistence avec Pickle

```python
from telegram.ext import PicklePersistence

# Créer persistence
persistence = PicklePersistence(filepath="bot_data.pickle")

# Créer l'application avec persistence
application = (
    Application.builder()
    .token("YOUR_BOT_TOKEN")
    .persistence(persistence)
    .build()
)

# Les données dans user_data et chat_data seront persistées automatiquement
```

## Webhooks

### Configuration Webhook (FastAPI)

```python
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application

app = FastAPI()

# Initialiser l'application Telegram
ptb_app = Application.builder().token("YOUR_BOT_TOKEN").build()

# Ajouter vos handlers
ptb_app.add_handler(CommandHandler("start", start))

@app.on_event("startup")
async def startup():
    """Configurer le webhook au démarrage"""
    await ptb_app.bot.set_webhook(
        url="https://your-domain.com/telegram",
        allowed_updates=Update.ALL_TYPES
    )
    await ptb_app.initialize()
    await ptb_app.start()

@app.on_event("shutdown")
async def shutdown():
    """Nettoyer au shutdown"""
    await ptb_app.stop()
    await ptb_app.shutdown()

@app.post("/telegram")
async def telegram_webhook(request: Request):
    """Handler pour le webhook Telegram"""
    update_dict = await request.json()
    update = Update.de_json(update_dict, ptb_app.bot)
    await ptb_app.process_update(update)
    return {"ok": True}
```

## Tools LangChain

### Intégration avec LangChain

```python
from langchain_core.tools import tool
from telegram import Bot
from telegram.constants import ParseMode

bot = Bot(token="YOUR_BOT_TOKEN")

@tool
async def send_telegram_notification(
    chat_id: str,
    message: str,
    parse_mode: str = "HTML"
) -> dict:
    """Envoie une notification Telegram.

    Args:
        chat_id: ID du chat destination
        message: Texte du message
        parse_mode: HTML ou Markdown

    Returns:
        Informations sur le message envoyé
    """
    sent_message = await bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode=ParseMode.HTML if parse_mode == "HTML" else ParseMode.MARKDOWN
    )

    return {
        "message_id": sent_message.message_id,
        "chat_id": sent_message.chat_id,
        "date": sent_message.date.isoformat()
    }

@tool
async def send_telegram_photo(
    chat_id: str,
    photo_url: str,
    caption: str = None
) -> dict:
    """Envoie une photo via Telegram."""
    sent_message = await bot.send_photo(
        chat_id=chat_id,
        photo=photo_url,
        caption=caption
    )

    return {
        "message_id": sent_message.message_id,
        "photo_file_id": sent_message.photo[-1].file_id
    }
```

## Bonnes Pratiques

### 1. Logging

```python
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"User {update.effective_user.id} started the bot")
    await update.message.reply_text("Welcome!")
```

### 2. Gestion d'Erreurs

```python
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler global pour les erreurs"""
    logger.error(f"Update {update} caused error {context.error}")

    # Notifier l'utilisateur
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "Sorry, an error occurred. Please try again later."
        )

application.add_error_handler(error_handler)
```

### 3. Rate Limiting

```python
from functools import wraps
from datetime import datetime, timedelta

user_last_message = {}
RATE_LIMIT = timedelta(seconds=1)

def rate_limit(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        now = datetime.now()

        if user_id in user_last_message:
            if now - user_last_message[user_id] < RATE_LIMIT:
                await update.message.reply_text("Please slow down!")
                return

        user_last_message[user_id] = now
        return await func(update, context)

    return wrapper

@rate_limit
async def command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Processing...")
```

## Ressources

- Documentation officielle: https://docs.python-telegram-bot.org
- Telegram Bot API: https://core.telegram.org/bots/api
- GitHub: https://github.com/python-telegram-bot/python-telegram-bot
- Examples: https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples

## Cas d'Usage du Projet

Dans ce boilerplate, Telegram est utilisé pour:

1. Notifications de workflows terminés
2. Alertes d'erreurs et monitoring
3. Interface conversationnelle pour déclencher des workflows
4. Envoi de rapports et résultats
5. Interactions utilisateur avec les agents LangChain
6. Commandes admin pour gérer le système
