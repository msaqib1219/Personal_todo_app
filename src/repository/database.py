"""Database engine and session factory."""

import os

from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine

from src.config import DATABASE_URL, logger


def create_engine_with_fallback(url: str | None = None):
    """Create SQLite engine. On corruption, recreate the database."""
    db_url = url or DATABASE_URL
    try:
        engine = create_engine(db_url, echo=False)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return engine
    except Exception:
        logger.warning("Database may be corrupted. Creating fresh database.")
        if ":///" in db_url and ":memory:" not in db_url:
            db_path = db_url.split(":///", 1)[1]
            if os.path.exists(db_path):
                os.remove(db_path)
        engine = create_engine(db_url, echo=False)
        return engine


def create_db_and_tables(engine):
    """Create all tables defined by SQLModel."""
    SQLModel.metadata.create_all(engine)


def get_session(engine) -> Session:
    """Create a new session."""
    return Session(engine)
