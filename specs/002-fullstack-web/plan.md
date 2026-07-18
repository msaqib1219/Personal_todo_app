# Implementation Plan: Full-Stack Web Application (Phase II)

**Branch**: `002-fullstack-web` | **Date**: 2026-03-02 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-fullstack-web/spec.md`

## Summary

Transform the Phase I local desktop todo app into a multi-user full-stack web application. The backend reuses the existing service/repository layer (adapted for PostgreSQL and multi-user), exposed via FastAPI REST API. The frontend is a Next.js 16 App Router application with Better Auth for authentication. Data persists in Neon Serverless PostgreSQL. JWT tokens issued by Better Auth are verified by FastAPI via JWKS endpoint.

## Technical Context

**Language/Version**: Python 3.13 (backend), TypeScript (frontend, Next.js 16)
**Primary Dependencies**:
- Backend: FastAPI, SQLModel, uvicorn, PyJWT, cryptography, python-dotenv, asyncpg
- Frontend: Next.js 16, React 19, better-auth, TypeScript, Tailwind CSS
**Storage**: Neon Serverless PostgreSQL (shared by both frontend auth tables and backend task tables)
**Testing**: pytest (backend), vitest or Jest (frontend)
**Target Platform**: Web browsers (desktop + mobile), deployed on Vercel (frontend) + any Python host (backend)
**Project Type**: Web (monorepo with frontend/ + backend/)
**Performance Goals**: Task list loads <2s for 500 tasks, task operations <500ms
**Constraints**: JWT-based auth, stateless backend, no server-side sessions
**Scale/Scope**: Multi-user, each user isolated, up to ~1000 users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The constitution (v1.1.0) is scoped to Phase I (local GUI app). Phase II fundamentally changes scope. Justified violations documented in Complexity Tracking below.

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Code Quality | PASS | Python backend follows same standards. TypeScript frontend adds ruff-equivalent (ESLint/Biome). |
| II. Test-First (TDD) | PASS | Backend tests via pytest. Frontend tests via vitest. Same Red-Green-Refactor cycle. |
| III. Simplicity (YAGNI) | PASS | Three layers preserved: API handler → service → repository. Frontend adds standard Next.js patterns. |
| IV. Security | PASS | JWT auth via JWKS (no shared secrets). Input validation server-side. SQL injection prevented via SQLModel ORM. No hardcoded secrets (.env). |
| V. Observability | PASS | Structured logging in FastAPI backend. Frontend console logging. |
| VI. Versioning | PASS | Semantic versioning. DB migrations via Alembic or manual scripts. Conventional Commits. |
| VII. Documentation | PASS | README updated with monorepo setup instructions. |

## Project Structure

### Documentation (this feature)

```text
specs/002-fullstack-web/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── service-contracts.md
└── tasks.md             # Phase 2 output (via /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── __init__.py
│   ├── config.py            # Environment config (DATABASE_URL, JWKS_URL, etc.)
│   ├── main.py              # FastAPI app entry point
│   ├── auth.py              # JWT verification middleware (JWKS-based)
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task SQLModel (extended with user_id)
│   ├── repository/
│   │   ├── __init__.py
│   │   ├── database.py      # PostgreSQL engine + session factory
│   │   └── task_repo.py     # TaskRepository (user-scoped queries)
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # TaskService (validation + business logic)
│   └── api/
│       ├── __init__.py
│       └── tasks.py         # Task REST endpoints (FastAPI router)
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   └── test_task_service.py
│   └── integration/
│       └── test_task_repo.py
├── pyproject.toml
├── .env.example
└── CLAUDE.md

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Landing/redirect
│   │   ├── (auth)/
│   │   │   ├── sign-in/page.tsx
│   │   │   └── sign-up/page.tsx
│   │   ├── dashboard/
│   │   │   └── page.tsx     # Main task list (protected)
│   │   └── api/
│   │       └── auth/
│   │           └── [...all]/route.ts  # Better Auth catch-all
│   ├── components/
│   │   ├── task-list.tsx
│   │   ├── task-card.tsx
│   │   ├── task-form.tsx
│   │   ├── task-filters.tsx
│   │   └── auth-guard.tsx
│   ├── lib/
│   │   ├── auth.ts          # Better Auth server instance
│   │   ├── auth-client.ts   # Better Auth client instance
│   │   └── api.ts           # Backend API client (fetch wrapper)
│   └── types/
│       └── task.ts          # Task TypeScript types
├── tests/
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.ts
├── .env.example
└── CLAUDE.md
```

**Structure Decision**: Web application (monorepo). Backend preserves Phase I's layered architecture (models → repository → services) with an added API layer. Frontend follows standard Next.js 16 App Router conventions.

## Complexity Tracking

> Constitution violations justified by Phase II scope change:

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Web frontend (constitution says "No web-based frontend") | Phase II hackathon requirement: Next.js frontend | Phase I scope was desktop-only; Phase II explicitly requires web |
| Multi-user auth (constitution says "No user authentication") | Phase II hackathon requirement: Better Auth with JWT | Single-user local app doesn't meet Phase II requirements |
| Cloud database (constitution says "SQLite local file") | Phase II hackathon requirement: Neon Serverless PostgreSQL | SQLite doesn't support concurrent multi-user web access |
| TypeScript addition (constitution specifies Python only) | Next.js frontend requires TypeScript | Python-only frontend frameworks don't meet hackathon requirements |

## Key Architecture Decisions

### 1. Auth Flow: JWKS-based JWT Verification
- Better Auth on Next.js issues JWTs (EdDSA/Ed25519 by default)
- Better Auth exposes JWKS endpoint at `/api/auth/jwks`
- FastAPI backend fetches JWKS to verify tokens — no shared secret needed
- Frontend attaches JWT in `Authorization: Bearer <token>` header

### 2. Database Strategy: Single Neon Instance
- Both Better Auth (user/session tables) and backend (task tables) use the same Neon PostgreSQL database
- Better Auth manages its own tables (user, session, account, verification)
- Backend manages the tasks table with `user_id` foreign key
- Connection: Backend uses SQLModel with `NullPool` + Neon's PgBouncer pooler endpoint

### 3. API Design: User ID from JWT (not URL)
- The hackathon spec shows `/api/{user_id}/tasks` but for security, the authenticated user_id comes from the verified JWT token, not the URL path
- API endpoints: `/api/tasks`, `/api/tasks/{id}`, `/api/tasks/{id}/complete`
- The JWT middleware extracts user_id and injects it into request state

### 4. Code Reuse from Phase I
- `TaskService` validation logic reused with minimal changes (add user_id parameter)
- `TaskRepository` adapted for PostgreSQL and user-scoped queries
- `Task` model extended with `user_id` field
- Business rules (recurrence, reminders) preserved
