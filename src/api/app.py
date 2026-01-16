from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.config.settings import settings
from src.config.database import init_db_connection, close_db_connection
from src.api.routes import chat, ingest

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize DB pool and checkpointer tables
    await init_db_connection()
    yield
    # Shutdown: Close DB pool
    await close_db_connection()

app = FastAPI(
    title=settings.APP_NAME,
    description="LangGraph Workflow API",
    version="0.1.0",
    debug=settings.DEBUG,
    lifespan=lifespan
)

app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(ingest.router, prefix="/api/v1", tags=["ingest"])

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "app_name": settings.APP_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)