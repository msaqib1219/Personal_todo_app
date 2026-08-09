import logging
from threading import Lock

from sqlalchemy.engine import Engine
from sqlalchemy.pool import NullPool
from sqlmodel import Session, SQLModel, create_engine

from src.config import config

logger = logging.getLogger(__name__)

_engine: Engine | None = None
_engine_lock = Lock()


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        with _engine_lock:
            if _engine is None:
                if not config.DATABASE_URL:
                    raise ValueError("DATABASE_URL not configured")
                _engine = create_engine(
                    config.DATABASE_URL,
                    poolclass=NullPool,
                    connect_args={"sslmode": "require"},
                    echo=False,
                )
    return _engine


def get_session():
    engine = get_engine()
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            logger.exception("Database session failed; rolling back")
            session.rollback()
            raise


def create_db_and_tables():
    engine = get_engine()
    try:
        SQLModel.metadata.create_all(engine)
    except Exception:
        logger.exception("Failed to create database tables")
        raise
