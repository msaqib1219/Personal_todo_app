from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.pool import NullPool
from sqlalchemy.engine import Engine
from src.config import config
from threading import Lock

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
        yield session


def create_db_and_tables():
    engine = get_engine()
    SQLModel.metadata.create_all(engine)