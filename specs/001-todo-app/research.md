# Research: Personal Todo APP

**Date**: 2026-02-22
**Feature**: 001-todo-app

## GUI Framework Selection

### Decision: CustomTkinter

**Rationale**: Best balance of modern look, zero system dependencies,
cross-platform reliability, and hackathon-pace simplicity. Built on
the battle-tested Tkinter stdlib with a modern flat design skin.

**Alternatives considered**:

| Framework | Pros | Cons | Rejected Because |
|-----------|------|------|------------------|
| Tkinter (stdlib) | Zero dependencies, stable | Dated 1990s appearance | Looks outdated; lacks modern widgets like scrollable frames |
| PySide6/Qt | Professional polish, mature | 150-200 MB install, system deps on Linux | Overkill for scope; installation friction at hackathon pace |
| Dear PyGui | GPU-accelerated, modern | Python 3.13 compat uncertain, slower dev pace | Risk of compatibility issues; immediate-mode paradigm adds learning curve |

**Key CustomTkinter advantages for this project**:
- `CTkScrollableFrame`: built-in scrollable container (no manual Scrollbar+Canvas boilerplate)
- `CTkCheckBox`: maps directly to task completion toggle
- `CTkEntry` / `CTkTextbox`: maps to task title/description input
- `CTkButton`: add/delete/save actions
- `CTkToplevel` / `CTkInputDialog`: confirmation and edit dialogs
- Dark/light mode auto-detection via `darkdetect`
- Install: `uv add customtkinter` (single command, ~2-3 MB, no C compilation)
- Bundle size: ~15-25 MB via PyInstaller if needed

## ORM / Database Layer

### Decision: SQLModel

**Rationale**: SQLModel combines SQLAlchemy's power with Pydantic
validation in a single model definition. For a simple single-entity
app, this eliminates the need for separate Pydantic schemas and
SQLAlchemy models.

**Alternatives considered**:

| Option | Pros | Cons | Rejected Because |
|--------|------|------|------------------|
| Raw sqlite3 | Zero deps, stdlib | Manual SQL, no validation | Violates Security principle (SQL injection risk from manual queries) |
| SQLAlchemy only | Mature, powerful | Separate validation layer needed | Extra boilerplate for a single-entity app |
| Peewee | Lightweight ORM | Less ecosystem support | SQLModel's Pydantic integration is more aligned with type-hint principle |

## Architecture Pattern

### Decision: Three-layer separation (GUI → Service → Repository)

**Rationale**: Constitution Principle III mandates maximum three layers.
This separation enables testing business logic without a GUI display
(Constitution Principle II: TDD).

- **GUI layer** (CustomTkinter): Thin presentation, event handling, widget rendering
- **Service layer**: Business logic (validation, ordering, state transitions)
- **Repository layer**: Database access via SQLModel/SQLite

## Logging

### Decision: Python `logging` module with RotatingFileHandler

**Rationale**: Constitution Principle V requires structured logging
to a configurable file location. The stdlib `logging` module is
sufficient; no need for `structlog` for this scope.

- Log to `~/.todo-app/app.log` (XDG-compliant on Linux, AppData on Windows)
- RotatingFileHandler to prevent unbounded log growth
- JSON-style log format for structured parsing
