from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from typing import Optional

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_current_client(api_key: str = Security(api_key_header)) -> str:
    """
    Validates the API key and returns the client_id.
    
    For V1 Prototype:
    We expect the API Key to follow the pattern: 'sk_{client_id}_{secret}'
    Example: 'sk_clientA_12345' -> client_id = 'clientA'
    
    In production, this would look up the key in a database.
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key header"
        )
        
    # Simple validation logic for prototype
    if not api_key.startswith("sk_"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key format"
        )
        
    try:
        # Extract client_id from 'sk_client_id_secret'
        parts = api_key.split("_")
        if len(parts) < 3:
             raise ValueError("Format too short")
        client_id = parts[1]
        return client_id
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
