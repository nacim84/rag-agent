# RAG Agent

## What This Is

A multi-tenant RAG (Retrieval Augmented Generation) system that enables external clients to query their business documents through natural language. Clients can ask questions, find specific documents (invoices, receipts, statements), and run calculations on structured data across three domains: accounting (comptable), transactions, and operations (exploitation). Migrated from an n8n workflow to Python/LangChain/LangGraph for production readiness.

## Core Value

External clients can get instant, accurate answers about their business documents through natural language queries, with proper isolation between client data.

## Requirements

### Validated

- LangGraph state machine architecture — existing
- FastAPI HTTP layer — existing
- PostgreSQL checkpointing for workflow persistence — existing
- Multi-LLM provider support (OpenAI, Anthropic, Gemini, Cohere) — existing
- Structured logging with structlog — existing
- Docker containerization — existing

### Active

- [ ] Multi-domain RAG routing (comptable/transaction/exploitation)
- [ ] Agent tools: RAG search with reranking, list documents, get file contents, SQL queries
- [ ] Chat memory per session (PostgreSQL)
- [ ] Multi-tenancy with `documents_{domain}_{client}` table pattern
- [ ] Document ingestion pipeline (upload, chunk, embed, store)
- [ ] Header API key authentication
- [ ] Production features: request validation, error handling, monitoring
- [ ] REST API endpoints for chat and ingestion

### Out of Scope

- Chat UI — API-only for now, frontend separate concern
- Real-time streaming responses — standard request/response sufficient for v1
- OAuth/JWT authentication — header API key sufficient for current clients
- Custom embedding models — Google Gemini embeddings as per existing n8n setup

## Context

**Migration source:** n8n workflow `Chat_RAG_Main.json` with:
- 3 specialized PGVector stores (comptable, transaction, exploitation)
- Google Gemini embeddings
- Cohere reranker (top 4)
- OpenRouter LLM (Grok) — will be configurable
- Postgres chat memory table `rag_chat_memory`
- Document metadata table `document_metadata`
- Structured data table `transaction_rows`

**Existing codebase:** LangGraph boilerplate with FastAPI, async PostgreSQL, multi-LLM support, Docker setup. Need to extend with RAG-specific components.

**External clients:** Business users querying their accounting, transaction, and operational documents. Each client has isolated vector tables.

## Constraints

- **Database**: Must connect to existing PostgreSQL with PGVector extension — data already populated
- **Table naming**: Client tables follow pattern `documents_{domain}_{client}` (e.g., `documents_comptable_clientA`)
- **Embeddings**: Google Gemini embeddings (must match existing vectors)
- **Reranker**: Cohere reranker for improved retrieval quality
- **Tech stack**: Python 3.11, LangChain, LangGraph, FastAPI as per existing boilerplate

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| LangGraph for orchestration | Already in boilerplate, good for complex agent workflows | — Pending |
| Flexible LLM provider | Decouple from specific provider, allow switching | — Pending |
| Separate tables per client | Client data isolation, existing pattern in production | — Pending |
| Header API key auth | Simple, matches existing n8n webhook pattern | — Pending |

---
*Last updated: 2026-01-16 after initialization*
