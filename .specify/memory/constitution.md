<!--
Sync Impact Report
===================
- Version change: 1.0.0 → 1.1.0 (MINOR: added Product Scope section,
  updated tech stack from FastAPI web API to GUI desktop app)
- Modified principles:
  - II. Test-First: removed API endpoint contract reference,
    added GUI interaction testing
  - IV. Security: removed CORS/JWT/OAuth2 web references,
    added local data protection
  - V. Observability: removed API endpoint logging and /health,
    added GUI-appropriate logging
  - VI. Versioning: removed API versioning, kept DB migrations
  - VII. Documentation: removed Swagger/OpenAPI references,
    added GUI usage instructions
- Added sections:
  - Product Scope (In Scope / Out of Scope)
- Removed sections: N/A
- Templates requiring updates:
  - .specify/templates/plan-template.md ✅ no update needed
    (Constitution Check section is dynamic)
  - .specify/templates/spec-template.md ✅ no update needed
    (template is principle-agnostic)
  - .specify/templates/tasks-template.md ✅ no update needed
    (task phases are dynamically generated)
- Follow-up TODOs: none
-->

# Personal Todo APP Constitution

## Product Scope

### In Scope

- **Add Task**: Create new todo items with title and details.
- **Delete Task**: Remove tasks from the list.
- **Update Task**: Modify existing task details.
- **View Task List**: Display all tasks in a scrollable list.
- **Mark as Complete**: Toggle task completion status.
- **GUI Interface**: Native desktop GUI (not web-based).
- **Cross-Platform**: MUST work on Linux and Windows.

### Out of Scope

- No web-based frontend (no browser UI, no REST/HTTP API).
- No mobile app.
- No user authentication or multi-user support (single local user).
- No real-time sync, WebSockets, or push notifications.
- No recurring todos, reminders, or scheduling.
- No file attachments.
- No sharing or team/collaboration features.
- No cloud deployment or server component.

## Core Principles

### I. Code Quality

All Python code MUST be clean, readable, and maintainable.

- Type hints MUST be used on all function signatures and return types.
- Code MUST pass `ruff check` and `ruff format` with zero violations.
- Functions MUST have a single responsibility and stay under 50 lines.
- Naming MUST be descriptive: no single-letter variables outside
  comprehensions and loop indices.
- Imports MUST be organized: stdlib, third-party, local (enforced by
  ruff isort rules).

**Rationale**: Consistent code quality reduces review friction and
enables confident refactoring during the hackathon's fast iteration
cycles.

### II. Test-First (TDD) (NON-NEGOTIABLE)

Tests MUST be written before implementation code.

- Red-Green-Refactor cycle is strictly enforced:
  1. Write a failing test that defines the desired behavior.
  2. Get user approval on the test.
  3. Confirm the test fails (Red).
  4. Write the minimum code to make the test pass (Green).
  5. Refactor while keeping tests green.
- `pytest` is the test runner. All tests reside under `tests/`.
- Critical paths MUST have tests; utility/helper code MAY skip tests
  if trivial.
- Integration tests MUST cover: database operations and data layer
  interactions.
- GUI logic MUST be separated from business logic so core
  functionality is testable without a display.

**Rationale**: TDD ensures correctness from the start and prevents
regressions as features are added rapidly.

### III. Simplicity (YAGNI)

The smallest viable solution MUST be preferred.

- No premature abstractions: three similar lines are better than a
  premature helper.
- No feature flags, backward-compatibility shims, or configuration
  for hypothetical futures.
- Direct implementation over clever patterns. If a design pattern is
  not solving a current problem, do not introduce it.
- Maximum three layers of abstraction for any operation
  (GUI handler → service → repository).

**Rationale**: Hackathon timelines demand focus on delivering working
features, not engineering for scale that may never arrive.

### IV. Security

Security basics MUST be enforced for local data protection.

- No hardcoded secrets, tokens, or credentials. All configuration
  MUST reside in `.env` files or config files (excluded from version
  control via `.gitignore`).
- All user input from GUI fields MUST be validated and sanitized
  before database writes.
- SQL injection MUST be prevented via parameterized queries or ORM
  usage (SQLAlchemy/SQLModel).
- Local database file MUST have appropriate file permissions.

**Rationale**: Even a local todo app stores personal data; basic
input validation and safe DB access prevent data corruption and
injection attacks.

### V. Observability

All runtime behavior MUST be inspectable without attaching a debugger.

- Structured logging MUST be used (Python `logging` module).
- Application MUST log: startup, shutdown, errors, and key user
  actions (task created, deleted, updated) at appropriate log levels.
- Errors MUST include stack traces and contextual data in logs.
- Logs MUST be written to a log file in a configurable location.

**Rationale**: When issues arise during demos or testing, structured
logs enable rapid diagnosis without restarting the application.

### VI. Versioning

All changes MUST be tracked with clear versioning.

- Project version follows Semantic Versioning (MAJOR.MINOR.PATCH) in
  `pyproject.toml`.
- Database schema changes MUST be versioned and reversible (Alembic
  or manual migration scripts).
- Git commits MUST follow Conventional Commits format:
  `type(scope): description` (e.g., `feat(todos): add priority field`).

**Rationale**: Clear versioning enables rollback, change tracking, and
team coordination even under time pressure.

### VII. Documentation

Documentation MUST be kept current and minimal.

- `README.md` MUST contain: project description, setup instructions,
  how to run the application, and supported platforms.
- Complex business logic MUST have inline comments explaining "why",
  not "what".
- No standalone documentation files unless explicitly requested.

**Rationale**: The README covers onboarding and usage; inline
comments capture intent. No API docs needed for a GUI app.

## Technology Constraints

- **Language**: Python 3.13
- **Package Manager**: uv
- **GUI Framework**: To be decided during planning (candidates:
  Tkinter, PySide6/Qt, CustomTkinter, Dear PyGui).
- **Testing**: pytest
- **Linting/Formatting**: ruff
- **Database**: SQLite (local file, via SQLAlchemy/SQLModel).
- **Target Platforms**: Linux, Windows.
- **Environment**: `.env` files or config files for settings.

## Development Workflow

- **Branch Strategy**: Feature branches from `main`; PRs required for
  merge.
- **Commit Style**: Conventional Commits
  (`feat`, `fix`, `docs`, `refactor`, `test`, `chore`).
- **Code Review**: All PRs MUST pass linting, formatting, and tests
  before merge.
- **Quality Gates**:
  1. `ruff check .` passes with zero errors.
  2. `ruff format --check .` passes with zero changes.
  3. `pytest` passes with zero failures.
- **Definition of Done**: Feature is implemented, tested, linted,
  and documented in README as applicable.

## Governance

This constitution is the authoritative source for project standards.
All development decisions MUST comply with these principles.

- **Amendments**: Any change to this constitution MUST be documented
  with rationale, approved by the project owner, and include a
  migration plan for existing code if applicable.
- **Versioning**: Constitution version follows Semantic Versioning:
  - MAJOR: Principle removed or fundamentally redefined.
  - MINOR: New principle or section added or materially expanded.
  - PATCH: Clarifications, wording fixes, non-semantic refinements.
- **Compliance Review**: At each milestone or PR, verify alignment
  with these principles. Non-compliance MUST be justified in the
  Complexity Tracking table of the implementation plan.
- **Conflict Resolution**: If a principle conflicts with a deadline,
  Simplicity (III) takes precedence, but Security (IV) is never
  compromised.

**Version**: 1.1.0 | **Ratified**: 2026-02-22 | **Last Amended**: 2026-02-22
