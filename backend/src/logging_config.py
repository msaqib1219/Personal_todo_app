import logging
import logging.handlers
import json
import sys
from pathlib import Path
from src.config import config

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "extra_data"):
            log_data["extra"] = record.extra_data
        return json.dumps(log_data)

def setup_logging() -> None:
    log_path = Path(config.LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, config.LOG_LEVEL))

    root_logger.handlers.clear()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(console_handler)

    file_handler = logging.handlers.RotatingFileHandler(
        log_path,
        maxBytes=10_485_760,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(file_handler)

    logging.getLogger("uvicorn.access").handlers = root_logger.handlers
    logging.getLogger("uvicorn.error").handlers = root_logger.handlers
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

def log_startup() -> None:
    logging.getLogger(__name__).info("Application starting", extra={"extra_data": {"config": {
        "database_url": config.DATABASE_URL[:20] + "...",
        "jwks_url": config.JWKS_URL,
        "frontend_url": config.FRONTEND_URL,
        "log_file": config.LOG_FILE,
    }}})

def log_shutdown() -> None:
    logging.getLogger(__name__).info("Application shutting down")