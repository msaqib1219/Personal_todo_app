# Tasks: Personal Todo APP

**Input**: Design documents from `/specs/001-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Included — constitution mandates TDD (Principle II, NON-NEGOTIABLE).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Project initialization and dependency installation

- [X] T001 Create project directory structure: `src/models/`, `src/repository/`, `src/services/`, `src/gui/`, `tests/unit/`, `tests/integration/`
- [X] T002 Update `pyproject.toml` with dependencies: customtkinter>=5.2.0, sqlmodel>=0.0.22, darkdetect>=0.8.0, and dev deps pytest>=8.0, ruff>=0.8.0
- [X] T003 Run `uv sync` to install all dependencies
- [X] T004 [P] Create `src/__init__.py`, `src/models/__init__.py`, `src/repository/__init__.py`, `src/services/__init__.py`, `src/gui/__init__.py`, `tests/__init__.py`, `tests/unit/__init__.py`, `tests/integration/__init__.py`
- [X] T005 [P] Configure ruff in `pyproject.toml`: enable isort rules, line-length=100, target Python 3.13

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can begin

**CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Implement app configuration in `src/config.py`: data directory path (`~/.todo-app/`), database path, log file path, auto-create directory on import, platform-aware path resolution
- [X] T007 Implement Task SQLModel entity in `src/models/task.py`: fields (id, title, description, is_completed, created_at, updated_at) per data-model.md with Field validators (min_length=1, max_length=500 on title)
- [X] T008 Implement database engine and session factory in `src/repository/database.py`: SQLite engine creation, `create_db_and_tables()` function, session dependency, corrupted DB fallback (create fresh + warn)
- [X] T009 Implement TaskRepository in `src/repository/task_repo.py` per contracts/service-contracts.md: `get_all()` (ORDER BY created_at DESC), `get_by_id()`, `create()`, `update()`, `toggle_completed()`, `delete()`
- [X] T010 Implement logging setup in `src/config.py`: RotatingFileHandler to `~/.todo-app/app.log`, JSON-style format, INFO level default, log startup/shutdown events
- [X] T011 Create shared test fixtures in `tests/conftest.py`: in-memory SQLite engine, session fixture, TaskRepository fixture, sample Task factory

### Tests for Foundational Phase

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation of T009**

- [X] T012 [P] Write integration tests for TaskRepository in `tests/integration/test_task_repo.py`: test create, get_all (ordering), get_by_id, update, toggle_completed, delete, get_by_id returns None for missing ID, delete returns False for missing ID

**Checkpoint**: Foundation ready — Task model, repository, config, logging, and test fixtures in place. User story implementation can now begin.

---

## Phase 3: User Story 1 — Add a New Task (Priority: P1) + User Story 2 — View Task List (Priority: P1) MVP

**Goal**: User can add tasks and see them in a persistent, scrollable list. This is the MVP.

**Independent Test**: Launch app, click "Add Task", enter title, confirm. Task appears in list. Close and reopen — task persists.

### Tests for US1+US2

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T013 [P] [US1] Write unit tests for TaskService.add_task in `tests/unit/test_task_service.py`: test valid title creates task, empty title raises ValueError, whitespace-only title raises ValueError, title >500 chars raises ValueError, optional description stored
- [X] T014 [P] [US2] Write unit tests for TaskService.list_tasks in `tests/unit/test_task_service.py`: test returns all tasks, ordered newest first, empty list returns []

### Implementation for US1+US2

- [X] T015 Implement TaskService.add_task and TaskService.list_tasks in `src/services/task_service.py`: title strip+validate (1-500 chars, no whitespace-only), delegate to TaskRepository, log actions
- [X] T016 Implement main application window in `src/gui/app.py`: CTk root window, title "Personal Todo APP", dark/light mode via `customtkinter.set_appearance_mode("system")`, window sizing
- [X] T017 [US1] Implement "Add Task" UI in `src/gui/app.py`: CTkEntry for title, CTkTextbox for description (optional), CTkButton "Add Task", validation error display, clear inputs on success
- [X] T018 [US2] Implement task list display in `src/gui/app.py`: CTkScrollableFrame showing all tasks, each task row with title text and completion checkbox (unchecked), newest first ordering, empty-state placeholder message ("No tasks yet. Click 'Add Task' to get started.")
- [X] T019 Implement `main.py` entry point: import config (triggers directory creation), initialize DB engine + create tables, create TaskRepository + TaskService, launch GUI app with service injected, log startup/shutdown

**Checkpoint**: US1+US2 functional — user can add tasks and view them in a persistent scrollable list. App can be launched and demoed as MVP.

---

## Phase 4: User Story 3 — Mark Task as Complete (Priority: P2)

**Goal**: User can toggle task completion status with visual feedback (checkmark + dimmed text).

**Independent Test**: Create a task, click the completion toggle, verify checkmark icon + greyed text. Toggle again to verify it reverts. Restart app and confirm status persists.

### Tests for US3

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T020 [P] [US3] Write unit tests for TaskService.toggle_task in `tests/unit/test_task_service.py`: test toggle incomplete→complete, toggle complete→incomplete, toggle missing task raises KeyError

### Implementation for US3

- [X] T021 [US3] Implement TaskService.toggle_task in `src/services/task_service.py`: delegate to repository toggle_completed, raise KeyError if not found, log action
- [X] T022 [US3] Update task list row in `src/gui/app.py` to support completion toggle: CTkCheckBox bound to toggle_task, completed tasks show checkmark icon + dimmed/greyed text (via CTkLabel configure fg_color), uncompleted tasks show normal text, refresh list after toggle

**Checkpoint**: US3 functional — completion toggle works with visual feedback and persists across restarts.

---

## Phase 5: User Story 4 — Update Task Details (Priority: P3)

**Goal**: User can edit a task's title and description via an edit dialog.

**Independent Test**: Create a task, double-click or select + "Edit", change title and description, save. Verify changes appear in list and persist after restart. Test cancel discards changes.

### Tests for US4

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T023 [P] [US4] Write unit tests for TaskService.update_task in `tests/unit/test_task_service.py`: test valid update changes title+description, empty title raises ValueError, missing task_id raises KeyError, updated_at timestamp changes

### Implementation for US4

- [X] T024 [US4] Implement TaskService.update_task in `src/services/task_service.py`: title strip+validate (same rules as add_task), delegate to repository update, raise KeyError if not found, log action
- [X] T025 [US4] Implement edit dialog in `src/gui/app.py`: CTkToplevel window with CTkEntry (title, pre-filled), CTkTextbox (description, pre-filled), Save and Cancel buttons, validation error display, refresh task list on save, close dialog on cancel without changes

**Checkpoint**: US4 functional — tasks can be edited with save/cancel behavior.

---

## Phase 6: User Story 5 — Delete a Task (Priority: P3)

**Goal**: User can delete a task with confirmation prompt.

**Independent Test**: Create a task, select it, click "Delete", confirm in dialog. Task disappears from list and is gone after restart. Test cancel keeps task.

### Tests for US5

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T026 [P] [US5] Write unit tests for TaskService.delete_task in `tests/unit/test_task_service.py`: test delete removes task, delete missing task_id raises KeyError

### Implementation for US5

- [X] T027 [US5] Implement TaskService.delete_task in `src/services/task_service.py`: delegate to repository delete, raise KeyError if not found, log action
- [X] T028 [US5] Implement delete UI in `src/gui/app.py`: "Delete" button on selected task or per-row delete icon, CTkMessagebox or CTkToplevel confirmation dialog ("Are you sure you want to delete this task?"), on confirm: call delete_task + refresh list, on cancel: close dialog

**Checkpoint**: US5 functional — tasks can be deleted with confirmation. All 5 user stories now work independently.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Edge cases, error handling, and final quality pass

- [X] T029 [P] Implement database corruption handling in `src/repository/database.py`: detect corrupted SQLite file on startup, create fresh DB, show warning to user via GUI messagebox
- [X] T030 [P] Implement title length enforcement in GUI: prevent input beyond 500 characters in CTkEntry (via validatecommand or StringVar trace) in `src/gui/app.py`
- [X] T031 [P] Add logging for all key user actions in `src/services/task_service.py`: task created (INFO), task updated (INFO), task toggled (INFO), task deleted (INFO), validation error (WARNING)
- [X] T032 Update `README.md` with: project description, prerequisites (Python 3.13, uv), setup instructions (`uv sync`), run instructions (`uv run python main.py`), supported platforms (Linux, Windows), data location (`~/.todo-app/`)
- [X] T033 Run full quality gates: `uv run ruff check .`, `uv run ruff format --check .`, `uv run pytest` — fix any failures
- [X] T034 Manual smoke test: launch app on current platform, perform full task lifecycle (add → view → mark complete → edit → delete), verify data persists across restart

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **US1+US2 (Phase 3)**: Depends on Foundational phase completion — this is the MVP
- **US3 (Phase 4)**: Depends on Phase 3 (needs task list to toggle)
- **US4 (Phase 5)**: Depends on Phase 3 (needs tasks to edit)
- **US5 (Phase 6)**: Depends on Phase 3 (needs tasks to delete)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **US1+US2 (P1)**: Can start after Foundational — No dependencies on other stories
- **US3 (P2)**: Depends on US1+US2 (needs task list with rows to toggle)
- **US4 (P3)**: Depends on US1+US2 (needs existing tasks to edit). Can run in parallel with US3 and US5
- **US5 (P3)**: Depends on US1+US2 (needs existing tasks to delete). Can run in parallel with US3 and US4

### Within Each User Story

1. Tests MUST be written and FAIL before implementation
2. Service layer before GUI layer
3. Core implementation before integration
4. Story checkpoint before moving to next priority

### Parallel Opportunities

- T004 + T005 (Setup: init files + ruff config)
- T012 + T013 + T014 (Tests: repo tests + service tests can be written in parallel)
- US4 (Phase 5) + US5 (Phase 6) can run in parallel after US3 is complete
- T029 + T030 + T031 (Polish: independent edge case tasks)

---

## Parallel Example: Phase 3 (US1+US2)

```bash
# Write all tests in parallel:
Task: "Unit tests for TaskService.add_task in tests/unit/test_task_service.py"
Task: "Unit tests for TaskService.list_tasks in tests/unit/test_task_service.py"

# Then implement service (sequential):
Task: "Implement add_task and list_tasks in src/services/task_service.py"

# Then implement GUI (sequential, depends on service):
Task: "Main window in src/gui/app.py"
Task: "Add Task UI in src/gui/app.py"
Task: "Task list display in src/gui/app.py"
Task: "Entry point in main.py"
```

---

## Implementation Strategy

### MVP First (US1+US2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: US1+US2 (Add + View)
4. **STOP and VALIDATE**: Launch app, add tasks, verify persistence
5. Deploy/demo if ready — this IS the MVP

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add US1+US2 → Test independently → Demo (MVP!)
3. Add US3 (Mark Complete) → Test independently → Demo
4. Add US4 (Update) + US5 (Delete) in parallel → Test → Demo
5. Polish phase → Final quality pass

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- US1 and US2 are combined into one phase because they are both P1 and tightly coupled (add needs view, view needs add)
- Each user story should be independently completable and testable
- Verify tests fail before implementing (Red-Green-Refactor)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
