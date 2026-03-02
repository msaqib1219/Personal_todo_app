# ADR-0001: GUI and ORM Technology Stack

- **Status:** Accepted
- **Date:** 2026-02-22
- **Feature:** 001-todo-app
- **Context:** The Personal Todo APP requires a cross-platform desktop GUI (Linux + Windows) with local SQLite persistence for up to 500 tasks. The project is built at hackathon pace with Python 3.13 and must support TDD by separating GUI from testable business logic. Key constraints: zero system-level dependencies for easy setup, modern visual appearance, and a three-layer architecture (GUI → Service → Repository) mandated by the constitution's simplicity principle.

## Decision

We adopt the following integrated technology stack:

- **GUI Framework**: CustomTkinter >=5.2.0 (modern Tkinter wrapper with flat design and dark/light mode)
- **Theme Detection**: darkdetect >=0.8.0 (auto-detect OS dark/light preference)
- **ORM**: SQLModel >=0.0.22 (SQLAlchemy + Pydantic in a single model definition)
- **Database Engine**: SQLite (local file at `~/.todo-app/tasks.db`)
- **Architecture Pattern**: Three-layer separation (GUI → Service → Repository) enabling full pytest coverage of business logic without a display

These components form a cohesive stack: CustomTkinter provides the presentation layer, SQLModel unifies data validation and persistence, and the three-layer pattern ensures they can be tested and evolved independently.

## Consequences

### Positive

- **Zero system dependencies**: `uv add customtkinter sqlmodel` installs everything. No C compilation, no system packages needed on Linux or Windows.
- **Modern appearance**: Flat design, rounded corners, dark/light mode auto-detection out of the box. The app will not look dated.
- **Purpose-built widgets**: `CTkScrollableFrame`, `CTkCheckBox`, `CTkEntry`, `CTkButton` map directly to todo app UI elements, reducing custom widget code.
- **Unified model layer**: SQLModel's single class serves as both the ORM entity and Pydantic validator, eliminating separate schema definitions for a single-entity app.
- **SQL injection prevention**: SQLAlchemy's parameterized queries (via SQLModel) satisfy the constitution's Security principle without manual effort.
- **Full testability**: Service and repository layers are pure Python with no GUI dependency; pytest with an in-memory SQLite database covers all business logic.
- **Small footprint**: ~2-3 MB for CustomTkinter, ~15-25 MB bundled via PyInstaller if distribution is needed.

### Negative

- **Single maintainer risk**: CustomTkinter is maintained by one developer (Tom Schimansky). If abandoned, the presentation layer needs migration. Mitigated: built on stable Tkinter stdlib, so fallback to raw Tkinter is feasible.
- **Limited advanced widgets**: CustomTkinter lacks complex widgets like tree views or data grids. Acceptable for this scope (flat task list only).
- **SQLModel maturity**: SQLModel is younger than SQLAlchemy and has fewer releases. Mitigated: for a single-entity app with basic CRUD, the API surface is small and stable.
- **No native OS integration**: Unlike PySide6/Qt, CustomTkinter does not provide native file dialogs or system tray icons. Not needed for this scope.

## Alternatives Considered

### Alternative Stack A: PySide6/Qt + SQLAlchemy

- **GUI**: PySide6 (Qt for Python) — professional polish, industrial-grade cross-platform
- **ORM**: SQLAlchemy with separate Pydantic schemas
- **Why rejected**: 150-200 MB install size, system dependency issues on Linux (libgl1, libxcb), overkill for a 5-operation todo app. The learning curve and setup friction conflict with hackathon-pace delivery.

### Alternative Stack B: Tkinter (stdlib) + Raw sqlite3

- **GUI**: Tkinter — zero dependencies, ships with Python
- **ORM**: None — direct sqlite3 module
- **Why rejected**: Dated 1990s appearance fails the modern look requirement. Raw SQL strings risk SQL injection, violating the Security constitution principle. Lacks `ScrollableFrame` widget, requiring manual Canvas+Scrollbar boilerplate.

### Alternative Stack C: Dear PyGui + Peewee

- **GUI**: Dear PyGui — GPU-accelerated, modern immediate-mode GUI
- **ORM**: Peewee — lightweight ORM
- **Why rejected**: Dear PyGui has uncertain Python 3.13 compatibility and a less conventional API paradigm. Peewee has a smaller ecosystem than SQLModel/SQLAlchemy. Combined risk is too high for hackathon delivery.

## References

- Feature Spec: [specs/001-todo-app/spec.md](../../specs/001-todo-app/spec.md)
- Implementation Plan: [specs/001-todo-app/plan.md](../../specs/001-todo-app/plan.md)
- Research: [specs/001-todo-app/research.md](../../specs/001-todo-app/research.md)
- Related ADRs: None (first ADR)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) (Principles III, IV governing this decision)
