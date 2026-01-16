from typing import TypedDict, Annotated, List, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """État partagé du graphe."""
    messages: Annotated[List[BaseMessage], add_messages]
    current_step: str
    context: dict
    error: Optional[str]
    final_output: Optional[dict]
