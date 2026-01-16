import sys
import logging
import structlog
from src.config.settings import settings

def configure_logging():
    """
    Configure structlog and standard logging.
    """
    # Shared processors for both standard logging and structlog
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    # Specific processors for structlog
    if settings.APP_ENV == "development":
        # Dev: Pretty console output
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer()
        ]
    else:
        # Prod: JSON output
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer()
        ]

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        cache_logger_on_first_use=True,
    )

    # Redirect standard logging to structlog
    # This captures logs from libraries (uvicorn, sqlalchemy, etc.)
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )
    
    # Optional: Lower level for third party libs if needed
    # logging.getLogger("uvicorn").setLevel(logging.INFO)

# Initial configuration on import
configure_logging()

def get_logger(name: str):
    return structlog.get_logger(name)
