from fastapi import FastAPI
from src.config.settings import settings
from src.api.routes import chat

app = FastAPI(
    title=settings.APP_NAME,
    description="LangGraph Workflow API",
    version="0.1.0",
    debug=settings.DEBUG
)

app.include_router(chat.router, prefix="/api/v1", tags=["chat"])

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "app_name": settings.APP_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
