# Personal Todo APP

A cross-platform desktop GUI todo application built with Python and CustomTkinter.

## About

**Personal Todo App** is a lightweight, efficient task management application designed for users who want a simple yet powerful way to organize their daily work. Built with **Python** (54.2% of codebase) and shell utilities (45.8%), this desktop application offers a distraction-free interface for capturing, tracking, and completing tasks.

Whether you're managing personal projects, work assignments, or daily chores, Personal Todo App provides an intuitive GUI with modern dark/light theme support and reliable persistent storage. The application runs natively on Linux and Windows, making it accessible across different platforms without compromise.

Core to the philosophy is simplicity: no complex hierarchies, no sync friction, no unnecessary features—just a clean database on your machine with the tools you need to get things done.

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
