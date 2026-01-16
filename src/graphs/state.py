from typing import TypedDict, Annotated, List, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from langchain_core.documents import Document

class AgentState(TypedDict):
    """
    Shared state for the RAG workflow.
    """
    # Core messages and identity
    messages: Annotated[List[BaseMessage], add_messages]
    client_id: str
    
    # RAG specific fields
    query: str
    domain: Optional[str]  # comptable, transaction, exploitation
    retrieved_docs: List[Document]
    
    # Execution state
    current_step: str
    context: dict
    error: Optional[str]
    
    # Output
    final_response: Optional[str]
    final_output: Optional[dict]  # Legacy support for boilerplate