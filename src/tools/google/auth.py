import os
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from src.config.settings import settings

# Scopes required for Drive and Sheets
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets',
]

def get_google_credentials():
    """
    Obtains Google credentials.
    Priority:
    1. Service Account (defined in settings.GOOGLE_SERVICE_ACCOUNT_PATH)
    2. OAuth2 Token (settings.GOOGLE_TOKEN_PATH)
    3. OAuth2 Flow (interactive, creates token)
    """
    creds = None

    # Option 1: Service Account (Preferred for Backend)
    # Check if path is set and file exists
    sa_path = settings.GOOGLE_SERVICE_ACCOUNT_PATH
    if sa_path and os.path.exists(sa_path):
        return service_account.Credentials.from_service_account_file(
            sa_path,
            scopes=SCOPES
        )

    # Option 2: OAuth2 User Credentials
    token_path = settings.GOOGLE_TOKEN_PATH
    
    if token_path and os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Refresh if expired
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        
    # Interactive Flow (Local Dev only)
    elif not creds:
        # Only run interactive flow if explicit credentials path is provided
        client_secrets_path = settings.GOOGLE_CREDENTIALS_PATH
        if client_secrets_path and os.path.exists(client_secrets_path):
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_path, SCOPES
            )
            creds = flow.run_local_server(port=0)
            
            # Save token for next time
            if token_path:
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
        else:
            # If no credentials found, return None or raise Error depending on usage
            return None

    return creds
