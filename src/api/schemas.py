from pydantic import BaseModel
from typing import List, Optional, Dict

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None

class SourceDocument(BaseModel):
    content: str
    metadata: Dict

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceDocument]
    session_id: str
    domain: Optional[str] = None
