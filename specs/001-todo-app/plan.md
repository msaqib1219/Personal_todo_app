# Implementation Plan: Personal Todo APP

**Branch**: `001-todo-app` | **Date**: 2026-02-22 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-todo-app/spec.md`

## Summary

Build a cross-platform (Linux + Windows) desktop GUI todo application
using Python 3.13, CustomTkinter for the UI, SQLModel/SQLite for
persistence, and a three-layer architecture (GUI → Service → Repository)
that enables full TDD of business logic without a display.

## Technical Context

**Language/Version**: Python 3.13
**Primary Dependencies**: CustomTkinter (GUI), SQLModel (ORM+validation), darkdetect (theme detection)
**Storage**: SQLite via SQLModel (local file at `~/.todo-app/tasks.db`)
**Testing**: pytest
**Target Platform**: Linux, Windows (desktop GUI)
**Project Type**: Single project
**Performance Goals**: App launch <3s, task operations <10s perceived
**Constraints**: Up to 500 tasks loaded in memory; no pagination
**Scale/Scope**: Single local user, 5 CRUD operations, 1 entity

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Code Quality | PASS | ruff check + format enforced via quality gates; type hints on all signatures per SQLModel/Pydantic |
| II. Test-First (TDD) | PASS | Three-layer architecture separates GUI from testable service/repo layers; pytest for all tests |
| III. Simplicity (YAGNI) | PASS | Three layers max (GUI → Service → Repository); no abstractions beyond what's needed |
| IV. Security | PASS | SQLModel prevents SQL injection; input validation in service layer; no hardcoded secrets |
| V. Observability | PASS | Python logging module with RotatingFileHandler to `~/.todo-app/app.log` |
| VI. Versioning | PASS | SemVer in pyproject.toml; Conventional Commits; DB schema created on first run |
| VII. Documentation | PASS | README with setup/run/platforms; quickstart.md generated; inline comments for complex logic |

**Gate result**: ALL PASS. No violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-app/
├── plan.md              # This file
├── research.md          # Phase 0: framework + ORM research
├── data-model.md        # Phase 1: Task entity schema
├── quickstart.md        # Phase 1: setup and run instructions
├── contracts/
│   └── service-contracts.md  # Phase 1: service layer interfaces
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
src/
├── models/
│   └── task.py          # Task SQLModel entity
├── repository/
│   └── task_repo.py     # TaskRepository: SQLite CRUD via SQLModel
├── services/
│   └── task_service.py  # TaskService: validation + business logic
├── gui/
│   └── app.py           # CustomTkinter application window
└── config.py            # App paths, logging setup, constants

tests/
├── unit/
│   └── test_task_service.py  # Service layer unit tests
├── integration/
│   └── test_task_repo.py     # Repository layer DB tests
└── conftest.py               # Shared fixtures (in-memory DB, etc.)

main.py                  # Entry point: initialize DB, launch GUI
```

**Structure Decision**: Single project layout. The `src/` directory
uses the three-layer split (models → repository → services → gui)
matching the Constitution's maximum three abstraction layers. Tests
mirror the source structure under `tests/`.

## Complexity Tracking

> No violations. Table intentionally empty.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| *(none)* | | |

## Architecture Overview

```text
┌─────────────────────────────────┐
│         main.py (entry)         │
│   - Init DB engine/session      │
│   - Configure logging           │
│   - Launch GUI                  │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│     GUI Layer (CustomTkinter)   │
│   - CTkScrollableFrame (list)   │
│   - CTkCheckBox (completion)    │
│   - CTkEntry (title input)      │
│   - CTkTextbox (description)    │
│   - CTkButton (add/delete/save) │
│   - CTkToplevel (edit dialog)   │
└──────────┬──────────────────────┘
           │ calls
           ▼
┌─────────────────────────────────┐
│     Service Layer               │
│   - TaskService                 │
│   - Input validation            │
│   - Business rules              │
│   - Error mapping               │
└──────────┬──────────────────────┘
           │ calls
           ▼
┌─────────────────────────────────┐
│     Repository Layer            │
│   - TaskRepository              │
│   - SQLModel session management │
│   - SQLite file I/O             │
└─────────────────────────────────┘
           │
           ▼
       ~/.todo-app/tasks.db
```

## Key Design Decisions

### 1. CustomTkinter for GUI

- Modern flat design with dark/light mode auto-detection
- `CTkScrollableFrame` eliminates manual scrollbar boilerplate
- Zero system dependencies (`uv add customtkinter`)
- ~2-3 MB installed; bundles at ~15-25 MB via PyInstaller
- See [research.md](research.md) for full comparison

### 2. SQLModel for persistence

- Single model definition serves as both ORM entity and Pydantic validator
- Prevents SQL injection via SQLAlchemy's parameterized queries
- `Field(min_length=1, max_length=500)` enforces title constraints
- See [data-model.md](data-model.md) for full schema

### 3. Platform-aware data directory

- Linux: `~/.todo-app/` (follows XDG convention)
- Windows: `~/.todo-app/` (simple, under user home)
- Both `tasks.db` and `app.log` stored here
- Directory auto-created on first run

### 4. Thin GUI, testable core

- GUI layer only handles widget rendering and event binding
- All validation and business logic in `TaskService`
- All DB access in `TaskRepository`
- Service and repository layers are fully testable with pytest
  using an in-memory SQLite database

## Dependencies

```toml
[project]
dependencies = [
    "customtkinter>=5.2.0",
    "sqlmodel>=0.0.22",
    "darkdetect>=0.8.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=8.0",
    "ruff>=0.8.0",
]
```

## Risk Analysis

| Risk | Impact | Mitigation |
|------|--------|------------|
| CustomTkinter maintained by single developer | Low (hackathon scope) | Built on stable Tkinter stdlib; could fall back to raw Tkinter if abandoned |
| SQLite concurrent access from multiple instances | Low | Edge case in spec; use file lock or single-instance check at startup |
| CustomTkinter theming inconsistency across Linux distros | Low | Test on Ubuntu/Debian; fall back to system theme if issues arise |
