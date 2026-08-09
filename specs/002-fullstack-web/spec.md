# Feature Specification: Full-Stack Web Application (Phase II)

**Feature Branch**: `002-fullstack-web`
**Created**: 2026-03-02
**Status**: Draft
**Input**: Transform the Todo app from a local CustomTkinter/SQLite desktop app into a multi-user full-stack web application with authentication, persistent cloud database, and responsive frontend.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration and Sign-In (Priority: P1)

A new user visits the Todo web app and creates an account with email and password. On subsequent visits, they sign in with their credentials. After signing in, they are redirected to their personal task dashboard. Unauthenticated users cannot access any task data.

**Why this priority**: Without authentication, the app cannot support multi-user isolation — the foundational requirement for a web-based todo app.

**Independent Test**: Can be tested by registering a new account, signing out, signing back in, and verifying the user lands on their dashboard. Delivers value: secure multi-user access.

**Acceptance Scenarios**:

1. **Given** no account exists, **When** user submits valid email and password on signup form, **Then** account is created and user is redirected to task dashboard.
2. **Given** an account exists, **When** user enters correct credentials, **Then** user is authenticated and sees their task list.
3. **Given** an account exists, **When** user enters wrong password, **Then** an error message is shown and no access is granted.
4. **Given** user is not signed in, **When** they navigate to the task dashboard URL, **Then** they are redirected to the sign-in page.

---

### User Story 2 - Task CRUD via Web Interface (Priority: P1)

An authenticated user can create, view, update, and delete tasks from a responsive web interface. Each task has a title (required), description (optional), priority, category, due date, recurrence, due time, and reminder minutes. The user only sees their own tasks.

**Why this priority**: Core functionality — the entire app exists to manage tasks.

**Independent Test**: Sign in, create a task, view it in the list, edit its title, delete it. Delivers value: full task management.

**Acceptance Scenarios**:

1. **Given** user is signed in, **When** they submit a new task with title "Buy groceries", **Then** the task appears in their task list with default priority "medium" and status incomplete.
2. **Given** a task exists, **When** user edits the title to "Buy organic groceries", **Then** the updated title is displayed.
3. **Given** a task exists, **When** user deletes it, **Then** it is removed from the list and cannot be retrieved.
4. **Given** user A creates a task, **When** user B signs in, **Then** user B does not see user A's task.

---

### User Story 3 - Toggle Task Completion (Priority: P1)

A user can mark a task as complete or incomplete. Completing a recurring task with a due date automatically creates the next occurrence.

**Why this priority**: Task completion is the core workflow loop of a todo app.

**Independent Test**: Create a task, toggle it complete, verify status changes. Create a recurring task with due date, complete it, verify next occurrence is created.

**Acceptance Scenarios**:

1. **Given** an incomplete task, **When** user marks it complete, **Then** the task shows as completed.
2. **Given** a completed task, **When** user marks it incomplete, **Then** the task shows as active.
3. **Given** a recurring weekly task due 2026-03-02, **When** user marks it complete, **Then** a new task is created with due date 2026-03-09 and same recurrence.

---

### User Story 4 - Search, Filter, and Sort Tasks (Priority: P2)

A user can search tasks by keyword, filter by status (active/completed), priority, or category, and sort by created date, due date, title, or priority.

**Why this priority**: Organization features make the app practical for users with many tasks, but the app is usable without them.

**Independent Test**: Create several tasks with different priorities and categories, use filters and search to narrow the list, sort by different columns.

**Acceptance Scenarios**:

1. **Given** tasks "Buy groceries" and "Read book" exist, **When** user searches "groceries", **Then** only "Buy groceries" is shown.
2. **Given** active and completed tasks exist, **When** user filters by status "active", **Then** only incomplete tasks are shown.
3. **Given** tasks with priority high and low, **When** user sorts by priority ascending, **Then** high-priority tasks appear first.

---

### User Story 5 - Responsive Web Interface (Priority: P2)

The web interface adapts to desktop, tablet, and mobile screen sizes. The layout is usable on all common devices.

**Why this priority**: A web app must be accessible across devices to be practical, but basic desktop functionality comes first.

**Independent Test**: Open the app on desktop (1920px), tablet (768px), and mobile (375px) widths and verify all features are accessible and readable.

**Acceptance Scenarios**:

1. **Given** a desktop browser, **When** viewing the task list, **Then** the layout uses available width with readable spacing.
2. **Given** a mobile browser, **When** viewing the task list, **Then** the layout stacks vertically and all buttons/inputs are tap-friendly.

---

### Edge Cases

- What happens when a user tries to create a task with an empty title? → Validation error shown, task not created.
- What happens when a user tries to access another user's task by ID? → 403 Forbidden or 404 Not Found.
- What happens when the database is unreachable? → User sees a friendly error message, no data loss.
- What happens when JWT token expires? → User is redirected to sign-in page.
- What happens when two users create tasks simultaneously? → Both succeed independently, no conflicts.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to register with email and password.
- **FR-002**: System MUST allow users to sign in with valid credentials and receive a session/token.
- **FR-003**: System MUST reject unauthenticated requests to task endpoints with 401 Unauthorized.
- **FR-004**: System MUST ensure each user can only access, create, modify, and delete their own tasks.
- **FR-005**: System MUST support creating tasks with: title (required, 1-500 chars), description (optional), priority (high/medium/low, default medium), category (work/home/personal/health/other, optional), due_date (optional), recurrence (daily/weekly/monthly/yearly, optional), due_time (HH:MM format, optional), reminder_minutes (non-negative integer, optional).
- **FR-006**: System MUST support listing tasks with filtering by status (active/completed/all), priority, category, and keyword search across title and description.
- **FR-007**: System MUST support sorting tasks by created date, due date, title, or priority in ascending or descending order.
- **FR-008**: System MUST support toggling a task's completion status.
- **FR-009**: System MUST automatically create the next occurrence when a recurring task with a due date is marked complete.
- **FR-010**: System MUST expose a RESTful API with endpoints for task CRUD and completion toggle.
- **FR-011**: System MUST persist all data in a cloud-hosted PostgreSQL database.
- **FR-012**: System MUST provide a responsive web frontend accessible on desktop and mobile browsers.
- **FR-013**: System MUST validate all inputs server-side (title length, priority values, time format, etc.).

### Key Entities

- **User**: Represents a registered person. Key attributes: unique identifier, email, name, creation timestamp. Managed by the authentication system.
- **Task**: Represents a todo item owned by one user. Key attributes: title, description, completion status, priority, category, due date, recurrence pattern, due time, reminder settings, creation/update timestamps. Belongs to exactly one user.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can register and sign in within 30 seconds on first attempt.
- **SC-002**: Users can create a new task in under 5 seconds (from clicking "add" to seeing it in the list).
- **SC-003**: Task list loads within 2 seconds for a user with up to 500 tasks.
- **SC-004**: All task operations (create, update, delete, toggle) are reflected immediately in the UI without full page reload.
- **SC-005**: Two different users signing in on separate browsers see only their own tasks with zero data leakage.
- **SC-006**: The interface is fully functional on screens from 375px to 1920px wide.
- **SC-007**: All existing task features (priorities, categories, search, filter, sort, recurrence, due dates, reminders) work identically in the web version as they did in the desktop version.

## Assumptions

- Better Auth is used for authentication on the frontend (Next.js), issuing JWT tokens that the backend verifies via JWKS endpoint (no shared secret).
- The backend (FastAPI) is a separate service from the frontend (Next.js), communicating via REST API.
- The monorepo structure has `frontend/` and `backend/` directories at the project root.
- Neon Serverless PostgreSQL is used as the cloud database.
- The existing Task model fields (from Phase I) are preserved and extended with a user_id foreign key.
- No email verification is required for registration (can be added later).
- Password requirements follow reasonable defaults (minimum 8 characters).

## Scope

### In Scope
- User registration and sign-in (email/password)
- JWT-based authentication between frontend and backend
- Full task CRUD with all existing fields
- Search, filter, sort functionality
- Recurring task auto-creation on completion
- Responsive web frontend
- RESTful API
- Cloud PostgreSQL database

### Out of Scope
- AI chatbot (Phase III)
- Kubernetes deployment (Phase IV)
- Email notifications or push notifications
- Social login (Google, GitHub, etc.)
- Password reset via email
- Real-time sync across multiple browser tabs
- Offline support
