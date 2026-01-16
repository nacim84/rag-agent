# Features Research: RAG Chat System

**Research Date:** 2026-01-16

## Table Stakes (Must Have)

### Retrieval
- **Vector similarity search** — core RAG functionality
- **Metadata filtering** — filter by client, domain, date, etc.
- **Reranking** — improve relevance after initial retrieval
- Complexity: Medium | Dependencies: Vector store, embeddings

### Query Handling
- **Domain routing** — route to appropriate vector store (comptable/transaction/exploitation)
- **Session context** — maintain conversation history
- Complexity: Medium | Dependencies: Chat memory

### Response Generation
- **Source attribution** — show which documents were used
- **Error handling** — graceful handling when no results found
- Complexity: Low | Dependencies: None

### Multi-tenancy
- **Client isolation** — each client only sees their data
- **API authentication** — verify client identity
- Complexity: High | Dependencies: Database schema

### Document Management
- **Ingestion pipeline** — upload, chunk, embed, store
- **Metadata extraction** — capture file info, dates, types
- Complexity: Medium | Dependencies: Vector store

## Differentiators (Nice to Have)

### Advanced Retrieval
- **Hybrid search** — combine vector + keyword search
- **Query reformulation** — improve unclear queries
- Complexity: Medium

### Response Quality
- **Confidence scoring** — indicate answer certainty
- **Follow-up suggestions** — suggest related questions
- Complexity: Low-Medium

### Structured Data
- **SQL queries** — query tabular data (existing in n8n)
- **Aggregations** — sums, counts, averages
- Complexity: Medium | Dependencies: transaction_rows table

## Anti-Features (Explicitly Don't Build)

- **Real-time streaming** — overkill for v1, adds complexity
- **Custom UI** — API-only, frontend is separate concern
- **Document editing** — read-only system
- **Cross-client analytics** — privacy violation risk

## Feature Dependencies

```
Authentication → Multi-tenancy
Vector Store → Retrieval → Reranking
Chat Memory → Session Context → Domain Routing
Ingestion Pipeline → Vector Store
```

---
*Features research: 2026-01-16*
