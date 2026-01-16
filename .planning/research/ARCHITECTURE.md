# Architecture Research: LangGraph RAG Agent

**Research Date:** 2026-01-16

## Component Overview

### Agent State Design

```python
class RAGAgentState(TypedDict):
    messages: Annotated[list, add_messages]  # Conversation history
    client_id: str                            # Multi-tenancy
    domain: Optional[str]                     # comptable/transaction/exploitation
    retrieved_docs: list[Document]            # RAG results
    query: str                                # Current user query
    final_response: Optional[str]             # Generated answer
    error: Optional[str]                      # Error state
```

### Workflow Structure

```
START
  ↓
[route_query] → Determine domain (comptable/transaction/exploitation)
  ↓
[retrieve] → Fetch from appropriate vector store
  ↓
[rerank] → Cohere reranking for relevance
  ↓
[generate] → LLM response with context
  ↓
END
```

### Tool Pattern

Use **retrievers as tools** — LangGraph ReAct pattern:
- Agent decides when to retrieve
- Multiple retrieval tools (one per domain)
- Agent can use SQL tool for structured queries

## Data Flow

```
API Request (chatInput, sessionId, client_id)
       ↓
[Authentication] → Validate API key, extract client_id
       ↓
[Load Memory] → Get conversation history for session
       ↓
[LangGraph Workflow]
       ↓
[Persist Memory] → Save new messages
       ↓
API Response (answer, sources)
```

## Component Boundaries

### API Layer (src/api/)
- Authentication middleware
- Request validation
- Response formatting
- Routes: /chat, /ingest, /documents

### RAG Layer (src/rag/)
- Retrievers (one per domain)
- Reranker wrapper
- Document loaders
- Chunking strategies

### Agent Layer (src/agents/)
- RAG workflow definition
- Tool definitions
- State management

### Data Layer (src/data/)
- Vector store client
- Chat memory repository
- Document metadata repository

## Build Order (Dependencies)

1. **Data Layer** — vector store client, memory repository
2. **RAG Layer** — retrievers, reranker (depends on data layer)
3. **Agent Layer** — workflow with tools (depends on RAG layer)
4. **API Layer** — routes, auth (depends on agent layer)
5. **Ingestion** — document pipeline (can parallel with 3-4)

## Integration Points

- **Existing checkpointer**: Use for workflow state, not chat memory
- **Existing settings**: Extend for new API keys (Cohere, Gemini)
- **Existing Docker**: Add new environment variables

---
*Architecture research: 2026-01-16*
