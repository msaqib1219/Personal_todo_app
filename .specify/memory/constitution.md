<!--
Sync Impact Report
===================
- Version change: 1.1.0 → 2.0.0 (MAJOR: expanded scope from Phase I
  desktop-only to include Phase II full-stack web application)
- Modified sections:
  - Product Scope: Split In Scope into Phase I + Phase II subsections
  - Product Scope: Updated Out of Scope for Phase II context
  - Technology Constraints: Split into Phase I, Phase II, and Shared
  - IV. Security: Expanded for web context (JWT, CORS, JWKS)
  - V. Observability: Added frontend logging guidance
  - VII. Documentation: Added API docs reference
- Added sections: N/A (expanded existing)
- Removed sections: N/A
- Templates requiring updates:
  - .specify/templates/plan-template.md ✅ no update needed
  - .specify/templates/spec-template.md ✅ no update needed
  - .specify/templates/tasks-template.md ✅ no update needed
- Follow-up TODOs: none
-->

# Personal Todo APP Constitution

## Product Scope

### In Scope

#### Phase I (Local Desktop App)
- **Add Task**: Create new todo items with title and details.
- **Delete Task**: Remove tasks from the list.
- **Update Task**: Modify existing task details.
- **View Task List**: Display all tasks in a scrollable list.
- **Mark as Complete**: Toggle task completion status.
- **GUI Interface**: Native desktop GUI (not web-based).
- **Cross-Platform**: MUST work on Linux and Windows.

#### Phase II (Full-Stack Web App)
- **Web Frontend**: Next.js 16 responsive web interface.
- **User Authentication**: Email/password registration and sign-in via Better Auth.
- **Multi-User Isolation**: Each user sees only their own tasks.
- **Cloud Database**: Neon Serverless PostgreSQL (shared by auth and task tables).
- **RESTful API**: FastAPI backend exposing task CRUD and completion toggle.
- **Recurring Tasks**: Auto-create next occurrence on completion.
- **Search/Filter/Sort**: Keyword search, status/priority/category filters, multi-field sorting.

### Out of Scope

- No AI chatbot (Phase III).
- No Kubernetes deployment (Phase IV).
- No email notifications or push notifications.
- No social login (Google, GitHub, etc.).
- No password reset via email.
- No real-time sync across browser tabs.
- No offline support.
- No file attachments.
- No sharing or team/collaboration features.

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

Security basics MUST be enforced for data protection.

- No hardcoded secrets, tokens, or credentials. All configuration
  MUST reside in `.env` files or config files (excluded from version
  control via `.gitignore`).
- All user input (GUI fields or API request bodies) MUST be validated
  and sanitized before database writes.
- SQL injection MUST be prevented via parameterized queries or ORM
  usage (SQLAlchemy/SQLModel).
- Phase I: Local database file MUST have appropriate file permissions.
- Phase II: JWT authentication via JWKS verification (no shared
  secrets between services). CORS MUST restrict origins to the
  frontend URL. All API endpoints MUST enforce user-scoped access.

**Rationale**: Data protection applies at every layer — local file
permissions for Phase I, JWT/CORS/user-scoping for Phase II.

### V. Observability

All runtime behavior MUST be inspectable without attaching a debugger.

- Structured logging MUST be used (Python `logging` module for
  backend; console logging for frontend).
- Application MUST log: startup, shutdown, errors, and key user
  actions (task created, deleted, updated) at appropriate log levels.
- Errors MUST include stack traces and contextual data in logs.
- Backend logs MUST be written to a log file in a configurable
  location (LOG_FILE env var).
- Frontend logging via browser console at appropriate levels.

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
- Phase II: FastAPI auto-generates OpenAPI docs at `/docs`; no
  separate API documentation files needed.

**Rationale**: The README covers onboarding and usage; inline
comments capture intent. Auto-generated API docs suffice for Phase II.

## Technology Constraints

### Phase I
- **Language**: Python 3.13
- **Package Manager**: uv
- **GUI Framework**: CustomTkinter
- **Database**: SQLite (local file, via SQLModel)
- **Target Platforms**: Linux, Windows

### Phase II
- **Backend**: Python 3.13, FastAPI, SQLModel, uvicorn, PyJWT, cryptography
- **Frontend**: TypeScript, Next.js 16, React 19, Better Auth, Tailwind CSS
- **Database**: Neon Serverless PostgreSQL (via psycopg + NullPool)
- **Package Managers**: uv (backend), npm (frontend)
- **Target Platforms**: Web browsers (desktop + mobile)

### Shared
- **Testing**: pytest (Python), vitest (TypeScript)
- **Linting/Formatting**: ruff (Python), Biome (TypeScript)
- **Environment**: `.env` files for settings (excluded from version control)

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

**Version**: 2.0.0 | **Ratified**: 2026-02-22 | **Last Amended**: 2026-03-05
