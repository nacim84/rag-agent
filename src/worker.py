from celery import Celery
from src.config.settings import settings

# Create Celery app
celery_app = Celery(
    "rag_worker",
    broker=settings.CELERY_BROKER_URL if hasattr(settings, "CELERY_BROKER_URL") else settings.REDIS_URL,
    backend=settings.CELERY_RESULT_BACKEND if hasattr(settings, "CELERY_RESULT_BACKEND") else settings.REDIS_URL
)

# Optional: Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Auto-discover tasks (if we had tasks packages)
# celery_app.autodiscover_tasks(['src.tasks'])

@celery_app.task
def health_check_task():
    """Simple task to verify worker is running."""
    return "Worker is healthy"
