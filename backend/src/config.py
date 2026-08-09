import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    JWKS_URL: str = os.getenv("JWKS_URL", "http://localhost:3000/api/auth/jwks")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    LOG_FILE: str = os.getenv("LOG_FILE", str(Path.home() / ".todo-app-web" / "app.log"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def reload(cls) -> None:
        cls.DATABASE_URL = os.getenv("DATABASE_URL", "")
        cls.JWKS_URL = os.getenv("JWKS_URL", "http://localhost:3000/api/auth/jwks")
        cls.FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
        cls.LOG_FILE = os.getenv("LOG_FILE", str(Path.home() / ".todo-app-web" / "app.log"))
        cls.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls) -> None:
        cls.reload()
        if not cls.DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is required")

config = Config()