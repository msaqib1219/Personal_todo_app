import pytest
from unittest.mock import Mock, patch
from sqlmodel import SQLModel, create_engine, Session
from src.repository.database import create_db_and_tables, get_session
from src.config import config


class TestDatabaseConnection:
    @pytest.fixture
    def test_engine(self):
        engine = create_engine("sqlite:///:memory:", echo=False)
        SQLModel.metadata.create_all(engine)
        return engine

    def test_engine_creation(self):
        from src.repository.database import engine
        assert engine is not None

    def test_session_factory_produces_working_sessions(self, test_engine):
        with Session(test_engine) as session:
            result = session.exec("SELECT 1").first()
            assert result == 1

    def test_table_creation_via_sqlmodel(self, test_engine):
        from src.models.task import Task
        inspector = __import__("sqlalchemy").inspect(test_engine)
        tables = inspector.get_table_names()
        assert "tasks" in tables