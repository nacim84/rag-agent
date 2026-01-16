# Stack Research: RAG System

**Research Date:** 2026-01-16

## Recommended Stack (2025)

### Vector Store
- **PGVector** (already in use) — PostgreSQL extension for vector similarity search
- Rationale: Already deployed with data, mature, good for multi-tenant isolation
- Confidence: High

### Embeddings
- **Google Gemini** (text-embedding-004) — already in use in n8n
- Rationale: Must match existing vectors, good multilingual support (French content)
- Alternative: OpenAI text-embedding-3-small if switching
- Confidence: High (must maintain compatibility)

### Reranking
- **Cohere Rerank** — already in use
- Rationale: Significantly improves retrieval quality, 10-20% relevance boost typical
- Version: cohere>=5.0.0, langchain-cohere>=0.3.0
- Confidence: High

### LLM Orchestration
- **LangChain** >=0.3.0 — RAG primitives, retrievers, chains
- **LangGraph** >=0.2.0 — already in use for workflow orchestration
- Rationale: Native integration, good tooling support
- Confidence: High

### Document Processing
- **LangChain text splitters** — RecursiveCharacterTextSplitter for general docs
- **Unstructured** — for complex document parsing (PDF, DOCX)
- Confidence: Medium (depends on document types)

### Chat Memory
- **PostgreSQL** — via existing checkpointer or custom table
- Rationale: Already have Postgres, keeps stack simple
- Confidence: High

## What NOT to Use

- **Pinecone/Weaviate/Qdrant** — already have PGVector with data
- **Custom embedding models** — must match existing vectors
- **LlamaIndex** — LangChain already in stack, avoid mixing

## Key Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| langchain | >=0.3.0 | Core RAG primitives |
| langchain-postgres | >=0.0.6 | PGVector integration |
| langchain-cohere | >=0.3.0 | Reranking |
| langchain-google-genai | >=2.0.0 | Embeddings |
| unstructured | >=0.15.0 | Document parsing |

---
*Stack research: 2026-01-16*
