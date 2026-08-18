# Phase II: Full-Stack Web Journey

> "From single-user desktop to multi-user cloud application — the same features, reimagined for the web."

## The Challenge

Phase II asked: take your desktop app and make it a web application.

But this wasn't a simple port. The requirements changed fundamentally:

| Aspect | Phase I | Phase II |
|--------|---------|----------|
| Users | Single | Multi-user |
| Storage | Local SQLite | Cloud PostgreSQL |
| Auth | None | JWT + Better Auth |
| Access | Local machine | Any browser |
| Database | File on disk | Neon Serverless |

## The Architecture Shift

### Desktop Architecture

```
User → GUI → Service → Repository → SQLite (local file)
```

### Web Architecture

```
User → Browser → Frontend (Next.js) → API → Backend (FastAPI) → Repository → Neon PostgreSQL
         ↑                                  ↑
         │                                  │
    Better Auth ←──────── JWT Token ────────┘
```

## Monorepo Decision

### Option A: Separate Repos

```
todo-frontend/    todo-backend/
├── src/          ├── src/
└── package.json  └── pyproject.toml
```

**Pros**: Clear separation, independent deployments  
**Cons**: Claude Code needs workspace setup, cross-cutting changes harder

### Option B: Monorepo ✅

```
To_do_App/
├── frontend/
├── backend/
├── specs/
└── CLAUDE.md
```

**Pros**: Single CLAUDE.md context, easier cross-cutting changes  
**Cons**: Larger repo

**Decision**: Monorepo. Claude Code works better when it sees the entire project.

## Backend Implementation

### The Stack

```python
# FastAPI + SQLModel + Neon PostgreSQL
from fastapi import FastAPI
from sqlmodel import SQLModel

app = FastAPI(title="Todo App API")
# ... CORS, routes, lifespan
```

### Key Files

| File | Purpose | Lines |
|------|---------|-------|
| `src/main.py` | FastAPI app entry point | 31 |
| `src/auth.py` | JWT verification via JWKS | 48 |
| `src/api/tasks.py` | REST endpoints | 103 |
| `src/services/task_service.py` | Business logic | 177 |
| `src/repository/task_repo.py` | Data access | 155 |
| `src/models/task.py` | SQLModel entity | 28 |

### Authentication Flow

```
1. User signs in on frontend
   ↓
2. Better Auth creates session + JWT token
   ↓
3. Frontend includes token in API requests
   ↓
4. Backend verifies token via JWKS endpoint
   ↓
5. Backend extracts user_id from token
   ↓
6. All queries filtered by user_id
```

### API Endpoints

```python
@router.get("/tasks")      # List tasks (filtered by user)
@router.post("/tasks")     # Create task
@router.get("/tasks/{id}") # Get single task
@router.put("/tasks/{id}") # Update task
@router.delete("/tasks/{id}") # Delete task
@router.patch("/tasks/{id}/complete") # Toggle completion
```

## Frontend Implementation

### The Stack

```typescript
// Next.js 16 + React 19 + Tailwind CSS
"use client";
import { useState } from "react";
// ... components
```

### Component Architecture

```
frontend/src/
├── app/
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Landing/redirect
│   ├── dashboard/page.tsx      # Main task dashboard
│   ├── (auth)/
│   │   ├── sign-in/page.tsx    # Sign-in page
│   │   └── sign-up/page.tsx    # Sign-up page
│   └── api/auth/[...all]/      # Better Auth route
├── components/
│   ├── auth-guard.tsx          # Protected route wrapper
│   ├── task-form.tsx           # Create/edit task form
│   ├── task-card.tsx           # Individual task display
│   ├── task-list.tsx           # Task list container
│   └── task-filters.tsx        # Filter/sort controls
└── lib/
    ├── auth.ts                 # Better Auth server
    ├── auth-client.ts          # Better Auth client
    └── api.ts                  # Backend API client
```

### The API Client

```typescript
// JWT Bearer token handling
async function apiRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = await getAuthToken();
  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  // ... fetch with error handling
}
```

## Specs Documentation

Phase II had comprehensive specs before implementation:

| Spec | Purpose |
|------|---------|
| `spec.md` | Feature specification with user stories |
| `plan.md` | Architecture and implementation plan |
| `data-model.md` | Database schema and relationships |
| `authentication-flow.md` | JWT + Better Auth integration |
| `frontend-architecture.md` | Component design and state management |
| `api-integration.md` | Frontend-backend contract |
| `responsive-design.md` | Mobile/tablet/desktop layouts |
| `testing-guide.md` | Test strategy and setup |
| `quickstart.md` | Developer onboarding |
| `research.md` | Technology evaluation |
| `tasks.md` | 55 tasks across 8 phases |

## Current State

### What's Done ✅

- Backend infrastructure (config, logging, database)
- JWT authentication via JWKS
- TaskService with full validation
- TaskRepository with CRUD
- All 6 REST API endpoints
- Backend unit + integration tests
- Frontend auth (sign-in, sign-up, auth guard)
- Frontend dashboard with task management
- All task components (form, card, list, filters)
- API client with JWT handling
- TypeScript types
- Responsive Tailwind CSS design

### What's Pending 🔄

- Neon PostgreSQL integration (currently SQLite fallback)
- Frontend testing (vitest)
- End-to-end integration testing
- Environment variable documentation
- UI polish and responsive testing

## Lessons from Phase II

### 1. Monorepos Work for AI

Claude Code navigated the monorepo seamlessly. It could see frontend and backend simultaneously, making cross-cutting changes easy.

### 2. Auth Is Harder Than It Looks

JWT verification via JWKS seemed simple. But:
- Token expiry handling
- CORS configuration
- User ID extraction
- Error responses

Each had edge cases the spec didn't mention.

### 3. Types Are Contracts

TypeScript types became the contract between frontend and backend. Changes in one required updates in the other.

### 4. Testing Multiplies Value

Backend tests caught issues before they reached the frontend. Integration tests verified the API contract.

## Files Created

```
backend/
├── src/
│   ├── main.py
│   ├── auth.py
│   ├── config.py
│   ├── logging_config.py
│   ├── api/tasks.py
│   ├── models/task.py
│   ├── repository/database.py, task_repo.py
│   └── services/task_service.py
└── tests/
    ├── unit/test_task_service.py, test_auth.py
    └── integration/test_task_repo.py, test_task_endpoints.py, test_database.py

frontend/
├── src/
│   ├── app/layout.tsx, page.tsx, error.tsx, global-error.tsx
│   ├── app/dashboard/page.tsx
│   ├── app/(auth)/sign-in/page.tsx, sign-up/page.tsx
│   ├── app/api/auth/[...all]/route.ts
│   ├── components/auth-guard.tsx, task-form.tsx, task-card.tsx, task-list.tsx, task-filters.tsx
│   ├── lib/auth.ts, auth-client.ts, api.ts, database.ts
│   └── types/task.ts
└── [config files: next.config.ts, tsconfig.json, biome.json, package.json]
```

---

**Next**: Phase III: AI Chatbot (Coming Soon) →
