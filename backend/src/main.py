from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import config
from src.logging_config import setup_logging, log_startup, log_shutdown
from src.repository.database import create_db_and_tables
from src.api.tasks import router as tasks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    log_startup()
    create_db_and_tables()
    yield
    log_shutdown()

app = FastAPI(
    title="Todo App API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks_router, prefix="/api")