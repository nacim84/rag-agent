# Google Workspace APIs - Compétences et Bonnes Pratiques

## Vue d'ensemble

Intégration avec Google Workspace (Drive, Gmail, Sheets) via les APIs Google. Support OAuth2 et Service Accounts pour l'authentification.

## Installation

```bash
uv add google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Configuration

### Variables d'Environnement

```env
# Chemin vers le fichier credentials OAuth2
GOOGLE_CREDENTIALS_PATH=/app/secrets/google_credentials.json
GOOGLE_TOKEN_PATH=/app/secrets/google_token.json

# Service Account (alternative)
GOOGLE_SERVICE_ACCOUNT_PATH=/app/secrets/service_account.json

# Scopes requis (séparés par virgule)
GOOGLE_SCOPES=https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/spreadsheets
```

### Scopes Disponibles

```python
SCOPES = [
    # Drive
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/drive.file',

    # Gmail
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',

    # Sheets
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/spreadsheets.readonly',

    # Calendar
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.readonly',
]
```

## Authentification

### OAuth2 (pour utilisateurs)

```python
# src/tools/google/auth.py
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/spreadsheets',
]

def get_google_credentials():
    """Obtient les credentials Google OAuth2."""
    creds = None
    token_path = os.getenv('GOOGLE_TOKEN_PATH')
    creds_path = os.getenv('GOOGLE_CREDENTIALS_PATH')

    # Charger depuis token existant
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Rafraîchir ou obtenir de nouveaux credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Sauvegarder les credentials
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds
```

### Service Account (pour automation)

```python
from google.oauth2 import service_account

def get_service_account_credentials():
    """Obtient les credentials via Service Account."""
    service_account_path = os.getenv('GOOGLE_SERVICE_ACCOUNT_PATH')

    credentials = service_account.Credentials.from_service_account_file(
        service_account_path,
        scopes=SCOPES
    )

    return credentials
```

### Fonction Unifiée

```python
def get_google_credentials():
    """Obtient les credentials Google (OAuth2 ou Service Account)."""

    # Option 1: Service Account
    if os.getenv('GOOGLE_SERVICE_ACCOUNT_PATH'):
        return service_account.Credentials.from_service_account_file(
            os.getenv('GOOGLE_SERVICE_ACCOUNT_PATH'),
            scopes=SCOPES
        )

    # Option 2: OAuth2
    return get_oauth2_credentials()
```

## Google Drive

### Tools LangChain pour Drive

```python
# src/tools/google/drive.py
from langchain_core.tools import tool
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from src.tools.google.auth import get_google_credentials
import os

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
        fields="files(id, name, mimeType, createdTime, modifiedTime)"
    ).execute()

    return results.get('files', [])

@tool
def search_drive_files(query: str, max_results: int = 10) -> list:
    """Recherche des fichiers dans Google Drive.

    Args:
        query: Requête de recherche (nom, type, etc.)
        max_results: Nombre max de résultats

    Returns:
        Liste des fichiers trouvés
    """
    creds = get_google_credentials()
    service = build('drive', 'v3', credentials=creds)

    results = service.files().list(
        q=f"name contains '{query}'",
        pageSize=max_results,
        fields="files(id, name, mimeType, webViewLink)"
    ).execute()

    return results.get('files', [])

@tool
def upload_to_drive(file_path: str, folder_id: str = None) -> dict:
    """Upload un fichier vers Google Drive.

    Args:
        file_path: Chemin du fichier local
        folder_id: ID du dossier de destination (optionnel)

    Returns:
        Informations sur le fichier uploadé
    """
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

@tool
def download_from_drive(file_id: str, destination_path: str) -> str:
    """Télécharge un fichier depuis Google Drive.

    Args:
        file_id: ID du fichier Google Drive
        destination_path: Chemin de destination local

    Returns:
        Chemin du fichier téléchargé
    """
    creds = get_google_credentials()
    service = build('drive', 'v3', credentials=creds)

    request = service.files().get_media(fileId=file_id)

    with open(destination_path, 'wb') as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()

    return destination_path
```

## Gmail

### Tools LangChain pour Gmail

```python
# src/tools/google/gmail.py
from langchain_core.tools import tool
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
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
def send_email_with_attachment(
    to: str,
    subject: str,
    body: str,
    attachment_path: str
) -> dict:
    """Envoie un email avec pièce jointe via Gmail."""
    creds = get_google_credentials()
    service = build('gmail', 'v1', credentials=creds)

    message = MIMEMultipart()
    message['to'] = to
    message['subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    # Ajouter la pièce jointe
    with open(attachment_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())

    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f'attachment; filename= {os.path.basename(attachment_path)}'
    )
    message.attach(part)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    sent = service.users().messages().send(
        userId='me',
        body={'raw': raw}
    ).execute()

    return sent

@tool
def search_emails(query: str, max_results: int = 10) -> list:
    """Recherche des emails dans Gmail.

    Args:
        query: Requête de recherche (ex: "from:user@example.com", "subject:important")
        max_results: Nombre max de résultats

    Returns:
        Liste des emails trouvés
    """
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
        detailed.append({
            'id': detail['id'],
            'snippet': detail['snippet'],
            'subject': next((h['value'] for h in detail['payload']['headers'] if h['name'] == 'Subject'), None),
            'from': next((h['value'] for h in detail['payload']['headers'] if h['name'] == 'From'), None),
        })

    return detailed
```

## Google Sheets

### Tools LangChain pour Sheets

```python
# src/tools/google/sheets.py
from langchain_core.tools import tool
from googleapiclient.discovery import build

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
    """Écrit des données dans Google Sheets.

    Args:
        spreadsheet_id: ID du spreadsheet
        range_name: Plage à écrire (ex: "Sheet1!A1")
        values: Données à écrire (liste de listes)

    Returns:
        Résultat de l'opération
    """
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

@tool
def append_to_spreadsheet(spreadsheet_id: str, range_name: str, values: list) -> dict:
    """Ajoute des données à la fin d'un Google Sheet.

    Args:
        spreadsheet_id: ID du spreadsheet
        range_name: Plage de départ (ex: "Sheet1!A1")
        values: Données à ajouter

    Returns:
        Résultat de l'opération
    """
    creds = get_google_credentials()
    service = build('sheets', 'v4', credentials=creds)

    body = {'values': values}

    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()

    return result

@tool
def create_spreadsheet(title: str, sheet_names: list = None) -> dict:
    """Crée un nouveau Google Spreadsheet.

    Args:
        title: Titre du spreadsheet
        sheet_names: Noms des feuilles à créer

    Returns:
        Informations sur le spreadsheet créé
    """
    creds = get_google_credentials()
    service = build('sheets', 'v4', credentials=creds)

    spreadsheet = {
        'properties': {'title': title}
    }

    if sheet_names:
        spreadsheet['sheets'] = [
            {'properties': {'title': name}} for name in sheet_names
        ]

    result = service.spreadsheets().create(
        body=spreadsheet,
        fields='spreadsheetId,spreadsheetUrl'
    ).execute()

    return result
```

## Bonnes Pratiques

### 1. Gestion des Credentials

```python
# Utiliser un cache pour les credentials
_credentials_cache = None

def get_google_credentials():
    global _credentials_cache
    if _credentials_cache and _credentials_cache.valid:
        return _credentials_cache

    _credentials_cache = _load_credentials()
    return _credentials_cache
```

### 2. Gestion des Erreurs

```python
from googleapiclient.errors import HttpError

@tool
def safe_drive_operation(file_id: str):
    """Opération Drive avec gestion d'erreur."""
    try:
        creds = get_google_credentials()
        service = build('drive', 'v3', credentials=creds)
        # ... opération
    except HttpError as error:
        if error.resp.status == 404:
            return {"error": "File not found"}
        elif error.resp.status == 403:
            return {"error": "Permission denied"}
        else:
            raise
```

### 3. Batch Requests

```python
from googleapiclient.http import BatchHttpRequest

def batch_delete_files(file_ids: list):
    """Supprimer plusieurs fichiers en batch."""
    service = build('drive', 'v3', credentials=get_google_credentials())

    batch = service.new_batch_http_request()

    for file_id in file_ids:
        batch.add(service.files().delete(fileId=file_id))

    batch.execute()
```

### 4. Rate Limiting

```python
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(
    wait=wait_exponential(multiplier=1, min=4, max=10),
    stop=stop_after_attempt(3)
)
def api_call_with_retry():
    """Appel API avec retry automatique."""
    pass
```

## Dépendances Requises

```toml
google-api-python-client>=2.100.0
google-auth-httplib2>=0.2.0
google-auth-oauthlib>=1.2.0
```

## Ressources

- Documentation Google APIs: https://developers.google.com/apis-explorer
- Python Client: https://github.com/googleapis/google-api-python-client
- OAuth2: https://developers.google.com/identity/protocols/oauth2

## Cas d'Usage du Projet

Google Workspace APIs sont utilisées pour:

1. Automatiser la création de rapports dans Sheets
2. Envoyer des notifications par Gmail
3. Synchroniser des documents Drive
4. Extraire des données de spreadsheets
5. Archiver des workflows dans Drive
6. Créer des workflows déclenchés par emails
