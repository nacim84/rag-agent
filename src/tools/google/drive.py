import io
import logging
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from src.tools.google.auth import get_google_credentials

logger = logging.getLogger(__name__)

class GoogleDriveClient:
    def __init__(self):
        self.creds = get_google_credentials()
        if not self.creds:
            logger.warning("Google Credentials not found. Drive features will be disabled.")
            self.service = None
        else:
            self.service = build('drive', 'v3', credentials=self.creds)

    def list_files(self, query: str = None, page_size: int = 10) -> List[Dict]:
        """
        List files from Google Drive.
        Args:
            query: Drive API query string (e.g., "name contains 'invoice'")
            page_size: Max results
        """
        if not self.service:
            return []

        # Default query: Not trashed
        full_query = "trashed = false"
        if query:
            full_query += f" and ({query})"

        results = self.service.files().list(
            q=full_query,
            pageSize=page_size,
            fields="nextPageToken, files(id, name, mimeType, modifiedTime)"
        ).execute()
        
        return results.get('files', [])

    def download_file(self, file_id: str) -> Optional[bytes]:
        """
        Download a file content as bytes.
        """
        if not self.service:
            return None

        try:
            request = self.service.files().get_media(fileId=file_id)
            file_io = io.BytesIO()
            downloader = MediaIoBaseDownload(file_io, request)
            
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                
            return file_io.getvalue()
        except Exception as e:
            logger.error(f"Failed to download file {file_id}: {e}")
            return None

# Singleton instance
drive_client = GoogleDriveClient()
