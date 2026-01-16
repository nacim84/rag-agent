# Research Summary: RAG Agent

**Research Date:** 2026-01-16

## Key Findings

### Stack
- **Keep existing**: PGVector, Google Gemini embeddings, Cohere reranker
- **Add**: langchain-postgres, langchain-cohere for LangChain integration
- **Avoid**: Don't switch embedding models (would require re-embedding all data)

### Table Stakes Features
1. Multi-tenant data isolation (critical)
2. Domain routing (comptable/transaction/exploitation)
3. Retrieval with reranking
4. Chat memory per session
5. Document ingestion pipeline
6. API authentication

### Architecture
- LangGraph workflow with retriever tools
- Separate layers: API → Agent → RAG → Data
- Build order: Data layer → RAG → Agent → API → Ingestion

### Critical Pitfalls to Avoid
1. **Data leakage** — Always filter by client_id, never expose cross-tenant data
2. **Embedding mismatch** — Must use same model as existing vectors
3. **SQL injection** — Parameterized queries only in SQL tool
4. **Memory bloat** — Limit conversation history length

## Recommended Approach

**Phase 1: Foundation**
- Data layer (vector store client, memory repo)
- Multi-tenant retriever with reranking
- Authentication middleware

**Phase 2: Agent Core**
- LangGraph workflow with RAG tools
- Domain routing logic
- Chat memory integration

**Phase 3: API & Ingestion**
- REST endpoints (/chat, /documents)
- Document ingestion pipeline
- Production hardening

## Files

| File | Content |
|------|---------|
| STACK.md | Technology recommendations |
| FEATURES.md | Feature categorization |
| ARCHITECTURE.md | System design |
| PITFALLS.md | Risk mitigation |

---
*Research complete: 2026-01-16*
