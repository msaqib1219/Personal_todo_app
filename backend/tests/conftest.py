import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.config import config


@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://test:test@localhost/test")
    monkeypatch.setenv("JWKS_URL", "http://localhost:3000/api/auth/jwks")
    monkeypatch.setenv("FRONTEND_URL", "http://localhost:3000")
    monkeypatch.setenv("LOG_FILE", "/tmp/test.log")
    config.validate()