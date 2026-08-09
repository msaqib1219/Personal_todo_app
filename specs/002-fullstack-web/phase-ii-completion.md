# Phase II Completion Specification

**Feature**: 002-fullstack-web  
**Date**: 2026-07-18  
**Status**: Draft

## Overview

This specification outlines the remaining work to complete Phase II of the todo application.

## Current State

### ✅ Completed

| Component | Status | Notes |
|-----------|--------|-------|
| Backend Infrastructure | ✅ Complete | config, logging, database, models |
| Backend Auth | ✅ Complete | JWT verification via JWKS |
| Backend Services | ✅ Complete | TaskService with validation |
| Backend Repository | ✅ Complete | TaskRepository with CRUD |
| Backend API | ✅ Complete | FastAPI endpoints |
| Backend Tests | ✅ Complete | Unit and integration tests |
| Project Structure | ✅ Complete | Monorepo with backend/frontend |
| Specs | ✅ Complete | Architecture, auth, UI, API, responsive |

### 🔄 Remaining Work

| Component | Status | Priority | Estimated Effort |
|-----------|--------|----------|------------------|
| Frontend Config | 🔄 Pending | High | 1 hour |
| Frontend Auth | 🔄 Pending | High | 3 hours |
| Frontend Dashboard | 🔄 Pending | High | 2 hours |
| Frontend Task Components | 🔄 Pending | High | 4 hours |
| Frontend API Client | 🔄 Pending | High | 2 hours |
| Frontend Testing | 🔄 Pending | Medium | 2 hours |
| Integration Testing | 🔄 Pending | Medium | 2 hours |
| Polish | 🔄 Pending | Low | 2 hours |

**Total Estimated Effort**: 18 hours

## Remaining Tasks

### Phase 2: Foundational (Frontend)

#### T014: Better Auth Server Config
**File**: `frontend/src/lib/auth.ts`

**Requirements**:
- Connect to Neon PostgreSQL
- Configure email/password provider
- Enable JWT plugin with JWKS endpoint
- Export auth instance

**Acceptance Criteria**:
- [ ] Auth instance created
- [ ] Database connection configured
- [ ] JWT plugin enabled
- [ ] Email/password provider configured

#### T015: Better Auth Client Config
**File**: `frontend/src/lib/auth-client.ts`

**Requirements**:
- Client-side auth hooks
- useSession, signIn, signUp, signOut
- Export auth client instance

**Acceptance Criteria**:
- [ ] Auth client created
- [ ] Hooks exported
- [ ] signIn function works
- [ ] signUp function works
- [ ] signOut function works
- [ ] useSession hook works

#### T016: Better Auth Catch-All Route
**File**: `frontend/src/app/api/auth/[...all]/route.ts`

**Requirements**:
- Export GET and POST handlers
- Route all auth requests to Better Auth

**Acceptance Criteria**:
- [ ] GET handler exported
- [ ] POST handler exported
- [ ] Auth requests routed correctly

#### T017: Root Layout
**File**: `frontend/src/app/layout.tsx`

**Requirements**:
- HTML structure
- Tailwind CSS setup
- Metadata (title, description)
- Global providers

**Acceptance Criteria**:
- [ ] HTML structure valid
- [ ] Tailwind CSS imported
- [ ] Metadata set
- [ ] Providers wrapped

#### T018: Backend API Client
**File**: `frontend/src/lib/api.ts`

**Requirements**:
- Fetch wrapper with JWT Bearer token
- Base URL from NEXT_PUBLIC_API_URL
- Handle 401 redirects
- Error handling

**Acceptance Criteria**:
- [ ] API client created
- [ ] JWT token attached
- [ ] 401 handling works
- [ ] Error handling implemented

#### T019: Task TypeScript Types
**File**: `frontend/src/types/task.ts`

**Requirements**:
- Task interface
- CreateTaskInput type
- UpdateTaskInput type
- TaskFilters type

**Acceptance Criteria**:
- [ ] Task interface defined
- [ ] CreateTaskInput defined
- [ ] UpdateTaskInput defined
- [ ] TaskFilters defined

#### T020: Next.js Config
**File**: `frontend/next.config.ts`

**Requirements**:
- Next.js configuration
- Environment variables
- Build settings

**Acceptance Criteria**:
- [ ] Config file created
- [ ] Environment variables configured
- [ ] Build settings correct

#### T021: TypeScript Config
**File**: `frontend/tsconfig.json`

**Requirements**:
- Strict TypeScript
- Path aliases
- Compiler options

**Acceptance Criteria**:
- [ ] Strict mode enabled
- [ ] Path aliases configured
- [ ] Compiler options set

#### T022: Tailwind Config
**File**: `frontend/tailwind.config.ts`

**Requirements**:
- Content paths
- Theme customization
- Plugins

**Acceptance Criteria**:
- [ ] Content paths set
- [ ] Theme customized
- [ ] Plugins configured

### Phase 3: User Story 1 (Auth)

#### T023: Sign-Up Page
**File**: `frontend/src/app/(auth)/sign-up/page.tsx`

**Requirements**:
- Email and password form
- Call Better Auth signUp
- Redirect to dashboard on success
- Show error on failure

**Acceptance Criteria**:
- [ ] Form renders
- [ ] Validation works
- [ ] signUp called
- [ ] Redirect on success
- [ ] Error on failure

#### T024: Sign-In Page
**File**: `frontend/src/app/(auth)/sign-in/page.tsx`

**Requirements**:
- Email and password form
- Call Better Auth signIn
- Redirect to dashboard on success
- Show error on invalid credentials

**Acceptance Criteria**:
- [ ] Form renders
- [ ] Validation works
- [ ] signIn called
- [ ] Redirect on success
- [ ] Error on failure

#### T025: Auth Guard Component
**File**: `frontend/src/components/auth-guard.tsx`

**Requirements**:
- Check session
- Redirect to sign-in if unauthenticated
- Render children if authenticated

**Acceptance Criteria**:
- [ ] Session check works
- [ ] Redirect works
- [ ] Children rendered

#### T026: Dashboard Page Shell
**File**: `frontend/src/app/dashboard/page.tsx`

**Requirements**:
- Wrap with auth-guard
- Display "Welcome" with user email
- Placeholder for task list

**Acceptance Criteria**:
- [ ] Auth guard applied
- [ ] Welcome message shown
- [ ] User email displayed

#### T027: Landing Page
**File**: `frontend/src/app/page.tsx`

**Requirements**:
- Redirect authenticated users to /dashboard
- Redirect unauthenticated to /sign-in

**Acceptance Criteria**:
- [ ] Auth check works
- [ ] Redirect to dashboard works
- [ ] Redirect to sign-in works

### Phase 4: User Story 2 (CRUD)

#### T034: Task Form Component
**File**: `frontend/src/components/task-form.tsx`

**Requirements**:
- Form with all task fields
- Submit calls API client POST /api/tasks
- Validation
- Loading state

**Acceptance Criteria**:
- [ ] Form renders all fields
- [ ] Validation works
- [ ] Submit calls API
- [ ] Loading state shows
- [ ] Success clears form

#### T035: Task Card Component
**File**: `frontend/src/components/task-card.tsx`

**Requirements**:
- Display task fields
- Edit button
- Delete button with confirmation
- Priority/category badges

**Acceptance Criteria**:
- [ ] Task fields displayed
- [ ] Edit button works
- [ ] Delete confirmation works
- [ ] Badges styled correctly

#### T036: Task List Component
**File**: `frontend/src/components/task-list.tsx`

**Requirements**:
- Fetch tasks via API client GET /api/tasks
- Render list of task-card components
- Show empty state when no tasks
- Loading state

**Acceptance Criteria**:
- [ ] Tasks fetched
- [ ] List rendered
- [ ] Empty state shown
- [ ] Loading state works

#### T037: Dashboard Integration
**File**: `frontend/src/app/dashboard/page.tsx`

**Requirements**:
- Add task-form for creation
- Add task-list for display
- Handle create/edit/delete with refetch

**Acceptance Criteria**:
- [ ] Task form integrated
- [ ] Task list integrated
- [ ] CRUD operations work

### Phase 5: User Story 3 (Toggle)

#### T040: Completion Toggle
**File**: `frontend/src/components/task-card.tsx`

**Requirements**:
- Checkbox or toggle button
- Call API client PATCH /api/tasks/{id}/complete
- Update UI to reflect new status

**Acceptance Criteria**:
- [ ] Toggle renders
- [ ] API called
- [ ] UI updates

#### T041: Task List Refresh
**File**: `frontend/src/components/task-list.tsx`

**Requirements**:
- After toggle, refetch task list
- Show newly created recurring task

**Acceptance Criteria**:
- [ ] List refreshes
- [ ] New task appears

### Phase 6: User Story 4 (Search/Filter/Sort)

#### T044: Task Filters Component
**File**: `frontend/src/components/task-filters.tsx`

**Requirements**:
- Search input
- Status filter
- Priority filter
- Category filter
- Sort field and direction

**Acceptance Criteria**:
- [ ] Search works
- [ ] Status filter works
- [ ] Priority filter works
- [ ] Category filter works
- [ ] Sort works

#### T045: Dashboard Filter Integration
**File**: `frontend/src/app/dashboard/page.tsx`

**Requirements**:
- Pass filter state to task-list
- Update API calls with query parameters

**Acceptance Criteria**:
- [ ] Filters connected
- [ ] API calls updated

### Phase 7: User Story 5 (Responsive)

#### T046-T050: Responsive Styles
**Files**: All components

**Requirements**:
- Tailwind responsive classes
- Mobile-friendly layouts
- Touch-friendly targets

**Acceptance Criteria**:
- [ ] Mobile layout works
- [ ] Tablet layout works
- [ ] Desktop layout works
- [ ] Touch targets adequate

### Phase 8: Polish

#### T051: Environment Variables
**Files**: backend/.env.example, frontend/.env.example

**Requirements**:
- All documented variables
- Correct defaults

**Acceptance Criteria**:
- [ ] All variables documented
- [ ] Defaults correct

#### T052: Error Boundary
**File**: `frontend/src/app/layout.tsx`

**Requirements**:
- Global error boundary
- Friendly error messages

**Acceptance Criteria**:
- [ ] Error boundary catches errors
- [ ] Friendly message shown

#### T053: JWT Token Expiry
**File**: `frontend/src/lib/api.ts`

**Requirements**:
- Detect 401 responses
- Redirect to sign-in

**Acceptance Criteria**:
- [ ] 401 detected
- [ ] Redirect works

#### T054: Logging Verification
**File**: Backend logs

**Requirements**:
- All key actions logged
- Appropriate log levels

**Acceptance Criteria**:
- [ ] Task CRUD logged
- [ ] Auth failures logged
- [ ] DB errors logged

#### T055: Quickstart Validation
**File**: specs/002-fullstack-web/quickstart.md

**Requirements**:
- Follow all steps
- Verify end-to-end works

**Acceptance Criteria**:
- [ ] Backend starts
- [ ] Frontend starts
- [ ] Auth flow works
- [ ] Task CRUD works

## Implementation Order

### Critical Path

1. **Phase 2 (Frontend Foundational)**
   - T019: Types (no dependencies)
   - T021: TypeScript config (no dependencies)
   - T022: Tailwind config (no dependencies)
   - T020: Next.js config (no dependencies)
   - T017: Root layout (depends on T021, T022)
   - T018: API client (depends on T019)
   - T014: Better Auth server (depends on T017)
   - T015: Better Auth client (depends on T017)
   - T016: Auth catch-all route (depends on T014)

2. **Phase 3 (Auth)**
   - T023: Sign-up page (depends on T015)
   - T024: Sign-in page (depends on T015)
   - T025: Auth guard (depends on T015)
   - T027: Landing page (depends on T025)
   - T026: Dashboard shell (depends on T025)

3. **Phase 4 (CRUD)**
   - T034: Task form (depends on T018, T019)
   - T035: Task card (depends on T019)
   - T036: Task list (depends on T018, T035)
   - T037: Dashboard integration (depends on T026, T034, T036)

4. **Phase 5 (Toggle)**
   - T040: Completion toggle (depends on T035)
   - T041: Task list refresh (depends on T036)

5. **Phase 6 (Search/Filter/Sort)**
   - T044: Task filters (depends on T019)
   - T045: Dashboard filter integration (depends on T037, T044)

6. **Phase 7 (Responsive)**
   - T046-T050: Responsive styles (depends on all components)

7. **Phase 8 (Polish)**
   - T051: Environment variables
   - T052: Error boundary
   - T053: JWT token expiry
   - T054: Logging verification
   - T055: Quickstart validation

## Parallel Opportunities

### Can Run in Parallel

- T019, T021, T022, T020 (all independent)
- T023, T024 (sign-up and sign-in pages)
- T034, T035 (task form and task card)
- T046-T050 (responsive styles on different components)

### Sequential Dependencies

- T017 → T014, T015, T016
- T015 → T023, T024, T025
- T025 → T026, T027
- T018, T019 → T034, T035
- T035 → T036
- T026, T034, T036 → T037
- T037, T044 → T045

## Risk Assessment

### High Risk

- **Better Auth Integration**: Complex configuration, may have issues
- **JWT Token Handling**: Security-critical, must work correctly
- **API Client Error Handling**: Must handle all edge cases

### Medium Risk

- **Responsive Design**: May need iteration
- **Form Validation**: Must match backend validation
- **State Management**: Must be consistent

### Low Risk

- **Styling**: Tailwind is straightforward
- **Type Definitions**: Simple interfaces
- **Config Files**: Standard setup

## Definition of Done

### For Each Task

- [ ] Code written
- [ ] Tests passing
- [ ] Linting passing
- [ ] Responsive on mobile/tablet/desktop
- [ ] Accessible (keyboard, screen reader)
- [ ] Error handling implemented
- [ ] Loading states implemented

### For Phase II

- [ ] All tasks complete
- [ ] All tests passing
- [ ] All linting passing
- [ ] End-to-end flow works
- [ ] Quickstart validation passed
- [ ] Demo ready

## Success Criteria

### Functional

- [ ] Users can sign up
- [ ] Users can sign in
- [ ] Users can create tasks
- [ ] Users can view tasks
- [ ] Users can edit tasks
- [ ] Users can delete tasks
- [ ] Users can toggle completion
- [ ] Users can search/filter/sort

### Non-Functional

- [ ] Responsive on all devices
- [ ] Accessible (WCAG 2.1 AA)
- [ ] Fast load times (< 2s)
- [ ] No console errors
- [ ] Secure (JWT, CORS, etc.)

### Demo Ready

- [ ] All features working
- [ ] Clean UI
- [ ] Error handling graceful
- [ ] Loading states smooth
- [ ] Mobile-friendly