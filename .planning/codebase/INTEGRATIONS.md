# External Integrations

**Analysis Date:** 2026-01-16

## LLM Providers

**OpenAI:**
- Purpose: Primary LLM for GPT models and embeddings
- SDK: `langchain-openai`
- Config: `src/config/settings.py`
- Env vars:
  - `OPENAI_API_KEY` - API authentication
  - `OPENAI_MODEL` - Model selection (default: gpt-4-turbo-preview)
  - `OPENAI_EMBEDDING_MODEL` - Embedding model (default: text-embedding-3-small)

**Anthropic:**
- Purpose: Claude models for LLM tasks
- SDK: `langchain-anthropic`
- Config: `src/config/settings.py`
- Env vars:
  - `ANTHROPIC_API_KEY` - API authentication
  - `ANTHROPIC_MODEL` - Model selection (default: claude-3-5-sonnet-20241022)

**Google AI:**
- Purpose: Gemini models for LLM and embeddings
- SDK: `langchain-google-genai`
- Config: `src/config/settings.py`
- Env vars:
  - `GOOGLE_API_KEY` - API authentication
  - `GOOGLE_MODEL` - Model selection (default: gemini-1.5-pro)

**Cohere:**
- Purpose: Reranking for RAG pipelines
- SDK: `langchain-cohere`, `cohere`
- Env vars:
  - `COHERE_API_KEY` - API authentication
  - `COHERE_RERANK_MODEL` - Model selection (default: rerank-english-v3.0)

## Observability

**LangSmith:**
- Purpose: LLM tracing, debugging, and monitoring
- SDK: `langsmith`
- Config: `src/config/settings.py`
- Env vars:
  - `LANGCHAIN_TRACING_V2` - Enable tracing (default: true)
  - `LANGCHAIN_ENDPOINT` - API endpoint
  - `LANGCHAIN_API_KEY` - API authentication
  - `LANGCHAIN_PROJECT` - Project name (default: rag-agent)

## Data Storage

**PostgreSQL:**
- Purpose: Primary relational database, LangGraph checkpointing
- Version: 16 (Alpine)
- Client: SQLAlchemy async with asyncpg driver
- Connection: `src/config/database.py`
- Env vars:
  - `DATABASE_URL` - Connection string (postgresql+asyncpg://...)
  - `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`
  - `POSTGRES_USER`, `POSTGRES_PASSWORD`
- Tables defined in `scripts/init_db.sql`:
  - `workflow_runs` - Workflow execution tracking
  - `integration_logs` - External service call logging
- Extensions enabled:
  - `uuid-ossp` - UUID generation
  - `pg_trgm` - Full-text search
  - `vector` (optional) - pgvector for embeddings

**Redis:**
- Purpose: Celery broker, result backend, caching
- Version: 7 (Alpine)
- Client: `redis` Python package
- Env vars:
  - `REDIS_URL` - General cache connection
  - `CELERY_BROKER_URL` - Task queue broker
  - `CELERY_RESULT_BACKEND` - Task result storage

**Vector Databases:**

*Qdrant (Optional):*
- Purpose: Vector similarity search
- Container: `qdrant/qdrant:latest`
- Ports: 6333 (HTTP), 6334 (gRPC)
- Env vars:
  - `QDRANT_HOST`, `QDRANT_PORT`, `QDRANT_API_KEY`

*Pinecone (External):*
- Purpose: Cloud vector database
- Env vars:
  - `PINECONE_API_KEY`
  - `PINECONE_ENVIRONMENT`
  - `PINECONE_INDEX_NAME`

*Supabase (External):*
- Purpose: PostgreSQL with pgvector
- Env vars:
  - `SUPABASE_URL`
  - `SUPABASE_KEY`
  - `SUPABASE_SERVICE_ROLE_KEY`

## Google Workspace

**Google Drive:**
- Purpose: File storage, document ingestion trigger
- SDK: `google-api-python-client`
- Auth: OAuth2 or Service Account
- Env vars:
  - `GOOGLE_CREDENTIALS_PATH` - OAuth2 credentials file
  - `GOOGLE_TOKEN_PATH` - OAuth2 token file
  - `GOOGLE_SERVICE_ACCOUNT_PATH` - Service account credentials
  - `GOOGLE_SCOPES` - API scopes

**Gmail:**
- Purpose: Email sending/receiving
- Scope: `https://www.googleapis.com/auth/gmail.modify`

**Google Sheets:**
- Purpose: Spreadsheet data access
- Scope: `https://www.googleapis.com/auth/spreadsheets`

## Messaging Platforms

**Telegram:**
- Purpose: Bot interactions
- SDK: `python-telegram-bot`
- Env vars:
  - `TELEGRAM_BOT_TOKEN` - Bot authentication
  - `TELEGRAM_WEBHOOK_URL` - Incoming webhook URL
  - `TELEGRAM_CHAT_ID` - Default chat destination

**WhatsApp (Meta Business API):**
- Purpose: Business messaging
- Env vars:
  - `WHATSAPP_PHONE_NUMBER_ID`
  - `WHATSAPP_BUSINESS_ACCOUNT_ID`
  - `WHATSAPP_ACCESS_TOKEN`
  - `WHATSAPP_VERIFY_TOKEN`
  - `WHATSAPP_WEBHOOK_URL`

**Slack:**
- Purpose: Workspace messaging and bots
- SDK: `slack-sdk`
- Env vars:
  - `SLACK_BOT_TOKEN` - Bot OAuth token
  - `SLACK_SIGNING_SECRET` - Request verification
  - `SLACK_APP_TOKEN` - App-level token

**Discord:**
- Purpose: Server bots
- Env vars:
  - `DISCORD_BOT_TOKEN`
  - `DISCORD_GUILD_ID`

## Workflow Automation

**N8N:**
- Purpose: Visual workflow automation
- Container: `n8nio/n8n:latest`
- Port: 5678
- Workflow: `n8n_assets/Add_Documents_Workflow.json`
- Env vars:
  - `N8N_BASE_URL`
  - `N8N_API_KEY`
  - `N8N_WEBHOOK_URL`
- Active workflow capabilities:
  - Google Drive file monitoring (create/update triggers)
  - Document extraction (Excel, CSV, PDF, Google Docs)
  - pgvector storage with Google Gemini embeddings
  - Text chunking with recursive character splitter
  - Multi-table vector storage (comptable, exploitation, transaction)

**Zapier:**
- Purpose: No-code automation webhooks
- Env vars:
  - `ZAPIER_WEBHOOK_URL`
  - `ZAPIER_NLA_API_KEY`

## Project Management

**Notion:**
- Purpose: Document database
- SDK: `notion-client`
- Env vars:
  - `NOTION_API_KEY`
  - `NOTION_VERSION` (default: 2022-06-28)
  - `NOTION_DATABASE_ID`

**Jira:**
- Purpose: Issue tracking
- Env vars:
  - `JIRA_BASE_URL`
  - `JIRA_EMAIL`
  - `JIRA_API_TOKEN`

**Linear:**
- Purpose: Issue tracking
- Env vars:
  - `LINEAR_API_KEY`

**Monday.com:**
- Purpose: Project management
- Env vars:
  - `MONDAY_API_KEY`

**Airtable:**
- Purpose: Spreadsheet database
- Env vars:
  - `AIRTABLE_API_KEY`
  - `AIRTABLE_BASE_ID`

## Communication Services

**Twilio:**
- Purpose: SMS and voice calls
- Env vars:
  - `TWILIO_ACCOUNT_SID`
  - `TWILIO_AUTH_TOKEN`
  - `TWILIO_PHONE_NUMBER`

**SendGrid:**
- Purpose: Transactional email
- Env vars:
  - `SENDGRID_API_KEY`

## Cloud Services

**AWS:**
- Purpose: S3 storage, potential compute
- Env vars:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_REGION` (default: eu-west-1)
  - `AWS_S3_BUCKET`

## Payment Processing

**Stripe:**
- Purpose: Payment processing
- Env vars:
  - `STRIPE_API_KEY`
  - `STRIPE_WEBHOOK_SECRET`

## Social Media

**Twitter/X:**
- Purpose: Social media integration
- SDK: `tweepy`

## Version Control

**GitHub:**
- Purpose: Repository webhooks
- Env vars:
  - `GITHUB_TOKEN`
  - `GITHUB_WEBHOOK_SECRET`

## Scheduling

**Calendly:**
- Purpose: Meeting scheduling
- Env vars:
  - `CALENDLY_API_KEY`

## Environment Configuration

**Required env vars for core functionality:**
```
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
```

**Required for LLM (at least one):**
```
OPENAI_API_KEY=sk-...
# or
ANTHROPIC_API_KEY=sk-ant-...
# or
GOOGLE_API_KEY=...
```

**Secrets location:**
- Environment variables via `.env` file
- Docker secrets mounted at `/app/secrets/`
- Google credentials at `/app/secrets/google_credentials.json`

## Webhooks

**Incoming Webhooks:**
- `/webhook/whatsapp` - WhatsApp Business API callbacks
- `/webhook/telegram` - Telegram bot updates
- Stripe webhook endpoint for payment events
- GitHub webhook for repository events

**Outgoing Webhooks:**
- N8N workflow triggers
- Zapier automation triggers

## N8N RAG Workflow Details

**File:** `n8n_assets/Add_Documents_Workflow.json`

**Triggers:**
- Google Drive file created/updated in monitored folders:
  - RAG_COMPTABLE folder
  - RAG_EXPLOITATION folder
  - RAG_TRANSACTION folder

**Processing:**
- File type detection (Excel, CSV, PDF, Google Docs)
- Document extraction via Docling chunker tool
- Text splitting: 2000 chars, markdown mode
- Embeddings: Google Gemini

**Storage:**
- PostgreSQL pgvector tables:
  - `documents_comptable`
  - `documents_exploitation`
  - `documents_transaction`
  - `document_metadata`
  - `transaction_rows`
  - `rag_chat_memory`

---

*Integration audit: 2026-01-16*
