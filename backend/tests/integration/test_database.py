import pytest
from unittest.mock import Mock, patch
from sqlalchemy import text
from sqlmodel import SQLModel, create_engine, Session
from src.repository.database import create_db_and_tables, get_session
from src.config import config


class TestDatabaseConnection:
    @pytest.fixture
    def test_engine(self):
        from src.models.task import Task  # noqa: F401 — register table in metadata

        engine = create_engine("sqlite:///:memory:", echo=False)
        SQLModel.metadata.create_all(engine)
        return engine

    def test_engine_creation(self):
        import src.repository.database as db

        db._engine = None
        engine = db.get_engine()
        assert engine is not None

    def test_session_factory_produces_working_sessions(self, test_engine):
        with Session(test_engine) as session:
            result = session.exec(text("SELECT 1")).first()
            assert result[0] == 1

    def test_table_creation_via_sqlmodel(self, test_engine):
        from src.models.task import Task

        inspector = __import__("sqlalchemy").inspect(test_engine)
        tables = inspector.get_table_names()
        assert "tasks" in tables
