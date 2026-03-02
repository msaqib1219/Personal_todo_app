# Personal Todo APP

A cross-platform desktop GUI todo application built with Python and CustomTkinter.

## Features

- Add, view, edit, and delete tasks
- Mark tasks as complete/incomplete with visual feedback
- Persistent SQLite storage
- Dark/light mode (follows system theme)
- Input validation (title: 1-500 characters)

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager

## Setup

```bash
uv sync
```

## Run

```bash
uv run python main.py
```

## Test

```bash
uv run pytest
```

## Lint

```bash
uv run ruff check .
uv run ruff format --check .
```

## Supported Platforms

- Linux
- Windows

## Data Location

All application data is stored in `~/.todo-app/`:
- `tasks.db` — SQLite database
- `app.log` — Application log file
