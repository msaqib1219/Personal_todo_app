"""App configuration: paths, logging setup, constants."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Data directory
DATA_DIR = Path.home() / ".todo-app"
DB_PATH = DATA_DIR / "tasks.db"
LOG_PATH = DATA_DIR / "app.log"

# Auto-create data directory
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Logging setup
logger = logging.getLogger("todo_app")
logger.setLevel(logging.INFO)

_handler = RotatingFileHandler(LOG_PATH, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
_handler.setFormatter(
    logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')
)
logger.addHandler(_handler)

# Suppress duplicate logs if root logger has handlers
logger.propagate = False

# Database URL
DATABASE_URL = f"sqlite:///{DB_PATH}"
