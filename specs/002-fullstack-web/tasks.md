# Tasks: Full-Stack Web Application (Phase II)

**Input**: Design documents from `/specs/002-fullstack-web/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/service-contracts.md, quickstart.md

**Tests**: Included per constitution Principle II (TDD, NON-NEGOTIABLE). Red phase tests written first, must fail before implementation.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, monorepo structure, dependency installation

- [x] T001 Create monorepo directory structure: `backend/src/`, `backend/src/models/`, `backend/src/repository/`, `backend/src/services/`, `backend/src/api/`, `backend/tests/`, `frontend/src/`, `frontend/src/app/`, `frontend/src/components/`, `frontend/src/lib/`, `frontend/src/types/`
- [ ] T002 [P] Initialize Python backend project with `backend/pyproject.toml` — dependencies: fastapi, sqlmodel, uvicorn, pyjwt, cryptography, python-dotenv, asyncpg, psycopg[binary], httpx; set `version = "0.1.0"`
- [ ] T002a [P] Configure ruff for backend in `backend/pyproject.toml` — add [tool.ruff] section with line-length=88, select rules (E, F, I, W), isort settings, format settings; verify `ruff check .` and `ruff format --check .` pass on empty project
- [ ] T003 [P] Initialize Next.js 16 frontend project with `frontend/package.json` — dependencies: next, react, better-auth, tailwindcss, typescript; set `"version": "0.1.0"`
- [ ] T003a [P] Configure Biome for frontend in `frontend/biome.json` — add linter and formatter rules for TypeScript/TSX; add `lint` and `format` scripts to `frontend/package.json`
- [ ] T004 [P] Create backend environment config template in `backend/.env.example` with DATABASE_URL, JWKS_URL, FRONTEND_URL
- [ ] T005 [P] Create frontend environment config template in `frontend/.env.example` with NEXT_PUBLIC_API_URL, DATABASE_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL
- [ ] T006 [P] Create `backend/CLAUDE.md` with backend-specific development instructions — include: run commands (`uv run uvicorn`, `uv run pytest`), key file locations, Conventional Commits requirement (`type(scope): description`)
- [ ] T007 [P] Create `frontend/CLAUDE.md` with frontend-specific development instructions — include: run commands (`npm run dev`, `npm test`), key file locations, Conventional Commits requirement (`type(scope): description`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 Implement environment configuration loader in `backend/src/config.py` — load DATABASE_URL, JWKS_URL, FRONTEND_URL, LOG_FILE (default `~/.todo-app-web/app.log`) from .env using python-dotenv
- [ ] T008a Implement structured logging module in `backend/src/logging_config.py` — configure Python logging with: JSON-structured format, configurable log file path (from LOG_FILE config), log levels (DEBUG/INFO/WARNING/ERROR), stdout + file handlers, startup/shutdown log entries
- [ ] T009 Implement PostgreSQL database engine and session factory in `backend/src/repository/database.py` — SQLModel with NullPool for Neon PgBouncer compatibility, SSL required
- [ ] T009a Create test infrastructure: `backend/tests/__init__.py`, `backend/tests/conftest.py` (shared fixtures: test DB session, mock JWT token), `backend/tests/unit/__init__.py`, `backend/tests/integration/__init__.py`
- [ ] T010 Create Task SQLModel in `backend/src/models/task.py` — all fields from data-model.md (id, user_id, title, description, is_completed, priority, category, due_date, recurrence, due_time, reminder_minutes, reminder_sent, created_at, updated_at) with proper constraints and indexes
- [ ] T011 Create `backend/src/models/__init__.py` exporting Task model
- [ ] T012 Implement JWT verification middleware in `backend/src/auth.py` — use PyJWKClient to fetch JWKS from JWKS_URL, verify EdDSA tokens, extract user_id from payload, inject into request state; return 401 on invalid/missing token
- [ ] T013 Create FastAPI app entry point in `backend/src/main.py` — configure CORS (allow FRONTEND_URL origin), include task router, add lifespan for DB table creation, mount auth dependency, configure logging on startup via logging_config
- [ ] T013a [P] Write backend unit test for JWT verification in `backend/tests/unit/test_auth.py` — test valid token returns user_id, expired token returns 401, missing token returns 401, invalid signature returns 401 (RED: all must fail before T012 implementation is verified)
- [ ] T013b [P] Write backend integration test for database connection in `backend/tests/integration/test_database.py` — test engine creation with valid URL, session factory produces working sessions, table creation via SQLModel (RED: must fail before T009 is verified)
- [ ] T014 [P] Configure Better Auth server instance in `frontend/src/lib/auth.ts` — connect to Neon PostgreSQL, configure email/password provider, enable JWT plugin with JWKS endpoint
- [ ] T015 [P] Configure Better Auth client instance in `frontend/src/lib/auth-client.ts` — client-side auth hooks (useSession, signIn, signUp, signOut)
- [ ] T016 Create Better Auth catch-all API route in `frontend/src/app/api/auth/[...all]/route.ts` — export GET and POST handlers
- [ ] T017 Create root layout in `frontend/src/app/layout.tsx` — HTML structure, Tailwind CSS setup, metadata
- [ ] T018 Create backend API client (fetch wrapper) in `frontend/src/lib/api.ts` — attach JWT Bearer token from session, base URL from NEXT_PUBLIC_API_URL, handle 401 redirects
- [ ] T019 Create Task TypeScript types in `frontend/src/types/task.ts` — matching backend Task model fields plus CreateTaskInput and UpdateTaskInput types
- [ ] T020 Create `frontend/next.config.ts` with any required Next.js configuration
- [ ] T021 Create `frontend/tsconfig.json` with strict TypeScript configuration and path aliases
- [ ] T022 Configure Tailwind CSS in `frontend/tailwind.config.ts` with content paths

**Checkpoint**: Foundation ready — database connected, auth configured on both sides, API client ready. User story implementation can now begin.

---

## Phase 3: User Story 1 — User Registration and Sign-In (Priority: P1) 🎯 MVP

**Goal**: Users can register with email/password, sign in, and be redirected to their dashboard. Unauthenticated users are redirected to sign-in.

**Independent Test**: Register a new account, sign out, sign back in, verify redirect to dashboard. Navigate to dashboard URL while logged out — verify redirect to sign-in.

### Implementation for User Story 1

- [ ] T023 [P] [US1] Create sign-up page in `frontend/src/app/(auth)/sign-up/page.tsx` — email and password form, call Better Auth signUp, redirect to dashboard on success, show error on failure
- [ ] T024 [P] [US1] Create sign-in page in `frontend/src/app/(auth)/sign-in/page.tsx` — email and password form, call Better Auth signIn, redirect to dashboard on success, show error on invalid credentials
- [ ] T025 [US1] Create auth guard component in `frontend/src/components/auth-guard.tsx` — check session, redirect to sign-in if unauthenticated, render children if authenticated
- [ ] T026 [US1] Create dashboard page shell in `frontend/src/app/dashboard/page.tsx` — wrap with auth-guard, display "Welcome" with user email, placeholder for task list
- [ ] T027 [US1] Create landing/redirect page in `frontend/src/app/page.tsx` — redirect authenticated users to /dashboard, unauthenticated to /sign-in

**Checkpoint**: User Story 1 complete — users can register, sign in, sign out, and access protected dashboard. Auth guard prevents unauthorized access.

---

## Phase 4: User Story 2 — Task CRUD via Web Interface (Priority: P1)

**Goal**: Authenticated users can create, view, edit, and delete tasks. Each user only sees their own tasks.

**Independent Test**: Sign in, create a task with title "Buy groceries", see it in the list, edit its title, delete it. Sign in as different user — verify no cross-user visibility.

### Backend Implementation

### Tests for User Story 2 (RED phase — must fail before implementation)

- [ ] T027a [P] [US2] Write unit tests for TaskService validation in `backend/tests/unit/test_task_service.py` — test title empty rejected, title >500 chars rejected, invalid priority rejected, invalid category rejected, invalid due_time format rejected, negative reminder_minutes rejected, valid input accepted
- [ ] T027b [P] [US2] Write integration tests for TaskRepository in `backend/tests/integration/test_task_repo.py` — test create task, get by id (own), get by id (other user returns None), list tasks (user-scoped), update task, delete task
- [ ] T027c [P] [US2] Write contract tests for task endpoints in `backend/tests/integration/test_task_endpoints.py` — test POST /api/tasks returns 201, GET /api/tasks returns user's tasks only, GET /api/tasks/{id} returns 404 for other user's task, PUT returns updated task, DELETE returns 204, all endpoints return 401 without token

### Backend Implementation

- [ ] T028 [US2] Implement TaskRepository in `backend/src/repository/task_repo.py` — user-scoped CRUD methods: create(user_id, data), get_by_id(user_id, task_id), list(user_id, filters), update(user_id, task_id, data), delete(user_id, task_id); all queries filter by user_id
- [ ] T029 [US2] Create `backend/src/repository/__init__.py` exporting TaskRepository
- [ ] T030 [US2] Implement TaskService in `backend/src/services/task_service.py` — validation logic (title 1-500 chars, valid priority/category/recurrence enums, due_time HH:MM format, reminder_minutes non-negative), call repository methods
- [ ] T031 [US2] Create `backend/src/services/__init__.py` exporting TaskService
- [ ] T032 [US2] Implement task REST endpoints in `backend/src/api/tasks.py` — FastAPI router with: GET /api/tasks (list), POST /api/tasks (create, 201), GET /api/tasks/{task_id} (get single), PUT /api/tasks/{task_id} (update), DELETE /api/tasks/{task_id} (204); all require auth dependency (401 without valid token), extract user_id from request state; return 404 (not 403) when task belongs to another user (prevents user_id enumeration)
- [ ] T033 [US2] Create `backend/src/api/__init__.py` and `backend/src/__init__.py` package init files

### Frontend Implementation

- [ ] T034 [US2] Create task-form component in `frontend/src/components/task-form.tsx` — form with fields: title (required), description, priority (select: high/medium/low), category (select: work/home/personal/health/other), due_date (date input), recurrence (select: daily/weekly/monthly/yearly), due_time (time input), reminder_minutes (number input); submit calls API client POST /api/tasks
- [ ] T035 [US2] Create task-card component in `frontend/src/components/task-card.tsx` — display task fields (title, priority badge, category, due date, status), edit button, delete button with confirmation
- [ ] T036 [US2] Create task-list component in `frontend/src/components/task-list.tsx` — fetch tasks via API client GET /api/tasks, render list of task-card components, show empty state when no tasks
- [ ] T037 [US2] Integrate task components into dashboard page in `frontend/src/app/dashboard/page.tsx` — add task-form for creation, task-list for display, handle create/edit/delete with optimistic UI updates or refetch

**Checkpoint**: User Story 2 complete — full task CRUD working end-to-end. Users create, view, edit, delete tasks. User isolation enforced by backend.

---

## Phase 5: User Story 3 — Toggle Task Completion (Priority: P1)

**Goal**: Users can mark tasks complete/incomplete. Completing a recurring task with a due date creates the next occurrence.

**Independent Test**: Create a task, toggle it complete, verify status changes. Create a recurring weekly task with due date 2026-03-02, complete it, verify new task created with due date 2026-03-09.

### Tests for User Story 3 (RED phase — must fail before implementation)

- [ ] T037a [P] [US3] Write unit test for recurrence logic in `backend/tests/unit/test_task_service.py` — test daily +1 day, weekly +7 days, monthly +1 month, yearly +1 year, no recurrence returns None
- [ ] T037b [P] [US3] Write contract test for toggle endpoint in `backend/tests/integration/test_task_endpoints.py` — test PATCH /api/tasks/{id}/complete toggles status, completing recurring task creates new task with advanced due_date

### Backend Implementation

- [ ] T038 [US3] Implement toggle completion endpoint PATCH /api/tasks/{task_id}/complete in `backend/src/api/tasks.py` — toggle is_completed; if completing + has recurrence + has due_date, call TaskService to create next occurrence with advanced due_date
- [ ] T039 [US3] Implement recurrence logic in `backend/src/services/task_service.py` — method to compute next due_date (daily +1 day, weekly +7 days, monthly +1 month, yearly +1 year) and create new task with same fields but new due_date and is_completed=false

### Frontend Implementation

- [ ] T040 [US3] Add completion toggle to task-card component in `frontend/src/components/task-card.tsx` — checkbox or toggle button, call API client PATCH /api/tasks/{id}/complete, update UI to reflect new status
- [ ] T041 [US3] Handle new recurring task in task-list in `frontend/src/components/task-list.tsx` — after toggle completion, refetch task list to show newly created recurring task occurrence

**Checkpoint**: User Story 3 complete — task completion toggle works, recurring tasks auto-create next occurrence.

---

## Phase 6: User Story 4 — Search, Filter, and Sort Tasks (Priority: P2)

**Goal**: Users can search tasks by keyword, filter by status/priority/category, and sort by various fields.

**Independent Test**: Create several tasks with different priorities/categories, search by keyword, filter by status "active", sort by priority.

### Tests for User Story 4 (RED phase — must fail before implementation)

- [ ] T041a [P] [US4] Write integration tests for filtered queries in `backend/tests/integration/test_task_repo.py` — test filter by status active/completed, filter by priority, filter by category, search by keyword (ILIKE), sort by created_at/due_date/title/priority asc/desc

### Backend Implementation

- [ ] T042 [US4] Implement query parameter filtering in GET /api/tasks endpoint in `backend/src/api/tasks.py` — accept status (all/active/completed), priority, category, search (ILIKE on title+description), sort_by (created_at/due_date/title/priority), sort_order (asc/desc) per contracts/service-contracts.md
- [ ] T043 [US4] Implement filtered/sorted query logic in `backend/src/repository/task_repo.py` — build dynamic SQLModel query with optional WHERE clauses and ORDER BY based on filter parameters

### Frontend Implementation

- [ ] T044 [US4] Create task-filters component in `frontend/src/components/task-filters.tsx` — search input, status filter (all/active/completed), priority filter dropdown, category filter dropdown, sort field and direction selectors
- [ ] T045 [US4] Integrate task-filters into dashboard in `frontend/src/app/dashboard/page.tsx` — pass filter state to task-list, update API calls with query parameters when filters change

**Checkpoint**: User Story 4 complete — search, filter, and sort all functional.

---

## Phase 7: User Story 5 — Responsive Web Interface (Priority: P2)

**Goal**: The interface adapts to desktop (1920px), tablet (768px), and mobile (375px) screen sizes.

**Independent Test**: Open app at desktop, tablet, and mobile widths — verify all features accessible and readable, buttons/inputs tap-friendly on mobile.

- [ ] T046 [US5] Apply responsive styles to task-list and task-card in `frontend/src/components/task-list.tsx` and `frontend/src/components/task-card.tsx` — Tailwind responsive classes for grid/stack layout, readable spacing at all breakpoints
- [ ] T047 [US5] Apply responsive styles to task-form in `frontend/src/components/task-form.tsx` — responsive form layout, tap-friendly inputs on mobile
- [ ] T048 [US5] Apply responsive styles to task-filters in `frontend/src/components/task-filters.tsx` — collapsible or stacked filters on mobile
- [ ] T049 [US5] Apply responsive styles to auth pages in `frontend/src/app/(auth)/sign-in/page.tsx` and `frontend/src/app/(auth)/sign-up/page.tsx` — centered card layout, mobile-friendly form
- [ ] T050 [US5] Apply responsive styles to dashboard layout in `frontend/src/app/dashboard/page.tsx` — proper padding, max-width container, mobile navigation

**Checkpoint**: User Story 5 complete — app usable on all screen sizes.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements affecting multiple user stories

- [ ] T051 [P] Verify and update `backend/.env.example` and `frontend/.env.example` to match all documented variables from quickstart.md (including LOG_FILE for backend)
- [ ] T052 [P] Add error boundary and friendly error messages for database unreachable / network errors in `frontend/src/app/layout.tsx` or a global error component
- [ ] T053 Handle JWT token expiry in `frontend/src/lib/api.ts` — detect 401 responses, redirect to sign-in page
- [ ] T054 [P] Verify logging coverage — confirm all key actions (task CRUD, auth failures, DB errors) produce structured log entries at appropriate levels in backend logs
- [ ] T055 Run quickstart.md validation — follow all steps in `specs/002-fullstack-web/quickstart.md` to verify end-to-end setup works

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 completion — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Phase 2 — auth infrastructure must be ready
- **User Story 2 (Phase 4)**: Depends on Phase 2 — can run in parallel with US1 (backend tasks are independent; frontend dashboard integration depends on US1's dashboard page T026)
- **User Story 3 (Phase 5)**: Depends on US2 (needs task CRUD endpoints and components)
- **User Story 4 (Phase 6)**: Depends on US2 (needs task listing endpoint and task-list component)
- **User Story 5 (Phase 7)**: Depends on US1–US4 components existing (applies responsive styles to them)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (Auth)**: Independent after Phase 2 — no dependency on other stories
- **US2 (CRUD)**: Backend independent after Phase 2; frontend dashboard integration depends on US1's page shell (T026)
- **US3 (Toggle)**: Depends on US2 task endpoints (T032) and task-card component (T035)
- **US4 (Search/Filter/Sort)**: Depends on US2 task listing endpoint (T032) and task-list component (T036)
- **US5 (Responsive)**: Depends on US1-US4 components existing to apply styles

### Within Each User Story

- Models before repositories
- Repositories before services
- Services before API endpoints
- Backend before frontend (frontend calls backend API)
- Core implementation before integration

### Parallel Opportunities

- **Phase 1**: T002, T003, T004, T005, T006, T007 all parallel
- **Phase 2**: T014, T015 parallel with each other; T008-T013 sequential (config → DB → model → auth → app)
- **Phase 3**: T023, T024 parallel (sign-up and sign-in pages)
- **Phase 4**: T028-T033 backend sequential; T034, T035 parallel (form and card); T036 depends on T035
- **Phase 6**: T042, T043 backend; T044 frontend parallel with backend
- **Phase 7**: T046, T047, T048, T049 all parallel (different files)
- **Phase 8**: T051, T052, T054 all parallel

---

## Parallel Example: User Story 2

```bash
# Backend (sequential — each depends on previous):
T028: TaskRepository in backend/src/repository/task_repo.py
T030: TaskService in backend/src/services/task_service.py
T032: Task endpoints in backend/src/api/tasks.py

# Frontend (can start T034, T035 in parallel once types exist):
T034: task-form component in frontend/src/components/task-form.tsx
T035: task-card component in frontend/src/components/task-card.tsx
# Then T036 depends on T035:
T036: task-list component in frontend/src/components/task-list.tsx
# Then T037 integrates all:
T037: Dashboard integration in frontend/src/app/dashboard/page.tsx
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 + 3)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1 (Auth)
4. Complete Phase 4: User Story 2 (CRUD)
5. Complete Phase 5: User Story 3 (Toggle Completion)
6. **STOP and VALIDATE**: Test all P1 stories independently
7. Deploy/demo if ready — this is a functional multi-user todo app

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 (Auth) → Users can register and sign in → Demo auth flow
3. Add US2 (CRUD) → Full task management → Demo core functionality (MVP!)
4. Add US3 (Toggle) → Task completion with recurrence → Demo completion workflow
5. Add US4 (Search/Filter/Sort) → Organization features → Demo filtering
6. Add US5 (Responsive) → Mobile-ready → Demo responsiveness
7. Polish → Production-quality → Final demo

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Backend endpoints designed per `contracts/service-contracts.md`
- Data model fields per `data-model.md`
- Environment setup per `quickstart.md`
- Total tasks: 67
