from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from uuid import uuid4

from src.api.schemas import ChatRequest, ChatResponse, SourceDocument
from src.api.auth import get_current_client
from src.agents.workflows.rag_workflow import create_rag_workflow
from langchain_core.messages import HumanMessage

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    client_id: str = Depends(get_current_client)
):
    """
    RAG Chat endpoint.
    Routes query -> Retrieves docs -> Reranks -> Generates answer.
    """
    try:
        # 1. Initialize Session
        session_id = request.session_id or str(uuid4())
        
        # 2. Create Workflow
        app = await create_rag_workflow()
        
        # 3. Prepare State
        initial_state = {
            "messages": [HumanMessage(content=request.query)],
            "query": request.query,
            "client_id": client_id,
            "current_step": "start",
            # Optional fields init
            "domain": None,
            "retrieved_docs": [],
            "error": None,
            "final_response": None,
            "context": {},
            "final_output": None
        }
        
        config = {"configurable": {"thread_id": session_id}}
        
        # 4. Execute Workflow
        final_state = await app.ainvoke(initial_state, config)
        
        # 5. Handle Errors
        if final_state.get("error"):
             raise HTTPException(status_code=500, detail=final_state["error"])

        # 6. Format Response
        sources = [
            SourceDocument(content=doc.page_content, metadata=doc.metadata)
            for doc in final_state.get("retrieved_docs", [])
        ]
        
        return ChatResponse(
            answer=final_state.get("final_response") or "No response generated.",
            sources=sources,
            session_id=session_id,
            domain=final_state.get("domain")
        )
        
    except Exception as e:
        # Log error here using structlog in future
        raise HTTPException(status_code=500, detail=str(e))
