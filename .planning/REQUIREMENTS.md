# Requirements: RAG Agent

**Defined:** 2026-01-16
**Core Value:** External clients can get instant, accurate answers about their business documents through natural language queries

## v1 Requirements

### Authentication

- [ ] **AUTH-01**: API validates X-API-Key header on all protected endpoints
- [ ] **AUTH-02**: API extracts client_id from authenticated request
- [ ] **AUTH-03**: All database queries filter by client_id (data isolation)

### Retrieval

- [ ] **RETR-01**: Agent routes queries to appropriate domain (comptable/transaction/exploitation)
- [ ] **RETR-02**: Vector search uses PGVector with client-specific tables
- [ ] **RETR-03**: Results are reranked using Cohere (top 4)
- [ ] **RETR-04**: Hybrid search combines vector similarity with keyword matching

### Agent Tools

- [ ] **TOOL-01**: RAG search tool retrieves from documents_{domain}_{client} tables
- [ ] **TOOL-02**: List Documents tool queries document_metadata filtered by client
- [ ] **TOOL-03**: Get File Contents tool extracts full document text by file_id
- [ ] **TOOL-04**: SQL Query tool executes queries on transaction_rows for client

### Chat Memory

- [ ] **CHAT-01**: Conversation history persisted per sessionId in PostgreSQL
- [ ] **CHAT-02**: Message history limited to prevent context bloat
- [ ] **CHAT-03**: Long conversations summarized to preserve context within limits

### Ingestion

- [ ] **INGST-01**: POST /ingest endpoint accepts document uploads
- [ ] **INGST-02**: Documents chunked and embedded with Google Gemini
- [ ] **INGST-03**: Chunks stored in client-specific vector table

### API Endpoints

- [ ] **API-01**: POST /chat accepts chatInput, sessionId, returns response with sources
- [ ] **API-02**: GET /documents returns document list for authenticated client
- [ ] **API-03**: POST /ingest processes and stores uploaded documents

### Production

- [ ] **PROD-01**: Structured logging for queries, retrievals, and errors
- [ ] **PROD-02**: Graceful error handling with user-friendly messages
- [ ] **PROD-03**: GET /health endpoint returns system status

## v2 Requirements

### Authentication
- **AUTH-04**: Rate limiting per client API key

### Ingestion
- **INGST-04**: PDF document parsing and extraction
- **INGST-05**: CSV/Excel parsing for structured data
- **INGST-06**: Automatic domain classification for uploads

### Advanced Retrieval
- **RETR-05**: Query reformulation for unclear questions
- **RETR-06**: Confidence scoring on responses

## Out of Scope

| Feature | Reason |
|---------|--------|
| Chat UI | API-only, frontend is separate project |
| Real-time streaming | Standard request/response sufficient for v1 |
| OAuth/JWT | Header API key matches existing n8n pattern |
| Custom embedding models | Must match existing Google Gemini vectors |
| Cross-client analytics | Privacy risk, explicitly excluded |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| AUTH-01 | Phase 1 | Pending |
| AUTH-02 | Phase 1 | Pending |
| AUTH-03 | Phase 1 | Pending |
| RETR-01 | Phase 2 | Pending |
| RETR-02 | Phase 1 | Pending |
| RETR-03 | Phase 1 | Pending |
| RETR-04 | Phase 2 | Pending |
| TOOL-01 | Phase 2 | Pending |
| TOOL-02 | Phase 2 | Pending |
| TOOL-03 | Phase 2 | Pending |
| TOOL-04 | Phase 2 | Pending |
| CHAT-01 | Phase 2 | Pending |
| CHAT-02 | Phase 2 | Pending |
| CHAT-03 | Phase 2 | Pending |
| INGST-01 | Phase 3 | Pending |
| INGST-02 | Phase 3 | Pending |
| INGST-03 | Phase 3 | Pending |
| API-01 | Phase 2 | Pending |
| API-02 | Phase 2 | Pending |
| API-03 | Phase 3 | Pending |
| PROD-01 | Phase 1 | Pending |
| PROD-02 | Phase 2 | Pending |
| PROD-03 | Phase 1 | Pending |

**Coverage:**
- v1 requirements: 22 total
- Mapped to phases: 22
- Unmapped: 0

---
*Requirements defined: 2026-01-16*
*Last updated: 2026-01-16 after initial definition*
