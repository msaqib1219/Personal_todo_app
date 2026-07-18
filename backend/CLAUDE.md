# Backend Development Guide

## Run Commands

```bash
# Install dependencies
uv sync

# Run development server
uv run uvicorn src.main:app --reload --port 8000

# Run tests
uv run pytest -x -q

# Lint and format
uv run ruff check .
uv run ruff format --check .
uv run ruff format .  # auto-fix
```

## Key File Locations

- `src/main.py` — FastAPI app entry point
- `src/config.py` — Environment configuration
- `src/auth.py` — JWT verification middleware
- `src/models/task.py` — Task SQLModel
- `src/repository/database.py` — Database engine + sessions
- `src/repository/task_repo.py` — TaskRepository (user-scoped)
- `src/services/task_service.py` — TaskService (validation + logic)
- `src/api/tasks.py` — REST endpoints
- `tests/` — All tests (unit/ and integration/)

## Conventions

- **Commits**: Conventional Commits format — `type(scope): description`
  - Examples: `feat(tasks): add CRUD endpoints`, `fix(auth): handle expired tokens`
- **Code Quality**: All code must pass `ruff check` and `ruff format` with zero violations
- **TDD**: Write failing tests first, then implement
- **Type Hints**: Required on all function signatures and return types
- **Functions**: Single responsibility, under 50 lines
