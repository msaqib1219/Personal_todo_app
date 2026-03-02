"""Shared test fixtures."""

from datetime import date

import pytest
from sqlmodel import Session, SQLModel, create_engine

from src.models.task import Task
from src.repository.task_repo import TaskRepository


@pytest.fixture
def engine():
    """In-memory SQLite engine for testing."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine):
    """Database session for testing."""
    with Session(engine) as session:
        yield session


@pytest.fixture
def repo(session):
    """TaskRepository instance for testing."""
    return TaskRepository(session)


@pytest.fixture
def sample_task(repo) -> Task:
    """Create and return a sample task."""
    return repo.create(
        title="Sample Task",
        description="A test task",
        priority="medium",
        category="work",
        due_date=date(2026, 6, 15),
    )
