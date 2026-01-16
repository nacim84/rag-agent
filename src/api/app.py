import time
import structlog
from uuid import uuid4
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from src.config.settings import settings
from src.config.database import init_db_connection, close_db_connection
from src.config.logging import get_logger, configure_logging
from src.api.routes import chat, ingest

# Initialize logging immediately
configure_logging()
logger = get_logger("api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("startup", app_env=settings.APP_ENV)
    await init_db_connection()
    yield
    await close_db_connection()
    logger.info("shutdown")

app = FastAPI(
    title=settings.APP_NAME,
    description="LangGraph Workflow API",
    version="0.1.0",
    debug=settings.DEBUG,
    lifespan=lifespan
)

# Middleware for Request Logging and ID
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid4())
    
    # Bind request_id to context for all subsequent logs in this request
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=request_id)
    
    start_time = time.time()
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log successful request
        logger.info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration=f"{process_time:.4f}s"
        )
        response.headers["X-Request-ID"] = request_id
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            "request_failed",
            method=request.method,
            path=request.url.path,
            error=str(e),
            duration=f"{process_time:.4f}s"
        )
        raise e

app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(ingest.router, prefix="/api/v1", tags=["ingest"])

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "app_name": settings.APP_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
