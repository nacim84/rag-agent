# Pitfalls Research: Multi-tenant RAG System

**Research Date:** 2026-01-16

## Critical Pitfalls

### 1. Multi-tenancy Data Leakage

**Risk:** Client A sees Client B's documents
**Warning Signs:**
- Queries without client_id filtering
- Hardcoded table names without client suffix
- Missing auth middleware

**Prevention:**
- Always filter by client_id in every query
- Use parameterized table names: `documents_{domain}_{client}`
- Auth middleware validates client_id matches API key
- Unit tests specifically for isolation

**Phase:** Address in Phase 1 (foundation)

### 2. Embedding Model Mismatch

**Risk:** New embeddings incompatible with existing vectors
**Warning Signs:**
- Zero or near-zero similarity scores
- Inconsistent retrieval quality
- Dimension mismatch errors

**Prevention:**
- Use exact same model as n8n: Google Gemini text-embedding-004
- Test with existing documents before bulk operations
- Store embedding model version in metadata

**Phase:** Address in Phase 1 (retriever setup)

### 3. Chat Memory Bloat

**Risk:** Sessions grow unbounded, slow performance
**Warning Signs:**
- Increasing latency over conversation
- Token limit errors
- Memory OOM

**Prevention:**
- Limit message history (last N messages or token window)
- Summarization for long conversations
- Session expiry/cleanup job

**Phase:** Address in Phase 2 (chat memory)

### 4. Poor Chunking Strategy

**Risk:** Documents chunked poorly, context lost
**Warning Signs:**
- Relevant info split across chunks
- Too many irrelevant results
- Incomplete answers

**Prevention:**
- Use semantic chunking for documents
- Preserve metadata (headers, sections)
- Test chunk sizes with real queries
- Include overlap between chunks

**Phase:** Address in Phase 3 (ingestion)

### 5. SQL Injection via RAG

**Risk:** Malicious queries in SQL tool
**Warning Signs:**
- Direct string interpolation in SQL
- Unbounded query results
- Schema exposure

**Prevention:**
- Parameterized queries only
- Whitelist allowed columns/tables
- Limit result size
- Validate client owns the file_id being queried

**Phase:** Address in Phase 2 (tools)

### 6. Reranker Latency

**Risk:** Cohere API adds significant latency
**Warning Signs:**
- >2s response times
- Timeouts during peak usage
- High API costs

**Prevention:**
- Cache reranked results for repeated queries
- Limit initial retrieval (top_k before rerank)
- Consider async reranking
- Monitor Cohere API response times

**Phase:** Address in Phase 1 (retriever)

## Medium Pitfalls

### 7. Domain Routing Errors
- LLM misclassifies query domain
- Prevention: Few-shot examples, fallback to multi-domain search

### 8. Missing Error Handling
- Unhandled exceptions crash workflow
- Prevention: Try/except in every node, graceful degradation

### 9. No Observability
- Can't debug retrieval issues
- Prevention: Log queries, retrieved docs, scores

---
*Pitfalls research: 2026-01-16*
