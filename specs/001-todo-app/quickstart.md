# Quickstart: Personal Todo APP

## Prerequisites

- Python 3.13+
- uv package manager

## Setup

```bash
# Clone and enter the project
git clone <repo-url>
cd "Hackathon II"

# Install dependencies
uv sync

# Run the application
uv run python main.py
```

## Development

```bash
# Run tests
uv run pytest

# Run linting
uv run ruff check .

# Run formatting check
uv run ruff format --check .

# Auto-fix formatting
uv run ruff format .
```

## Project Structure

```text
src/
├── models/
│   └── task.py          # Task SQLModel entity
├── repository/
│   └── task_repo.py     # Database access layer
├── services/
│   └── task_service.py  # Business logic and validation
├── gui/
│   └── app.py           # CustomTkinter GUI application
└── config.py            # App configuration (paths, logging)

tests/
├── unit/
│   └── test_task_service.py
├── integration/
│   └── test_task_repo.py
└── conftest.py          # Shared fixtures

main.py                  # Application entry point
```

## Data Location

- **Database**: `~/.todo-app/tasks.db`
- **Logs**: `~/.todo-app/app.log`

## Supported Platforms

- Linux (tested on Debian/Ubuntu)
- Windows 10/11
