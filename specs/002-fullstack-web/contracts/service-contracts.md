# API Contracts: Full-Stack Web Application (Phase II)

**Feature**: 002-fullstack-web
**Date**: 2026-03-02

## Authentication

All task endpoints require a valid JWT token in the `Authorization` header:
```
Authorization: Bearer <jwt-token>
```

The backend extracts `user_id` from the verified JWT payload. Requests without a valid token receive `401 Unauthorized`.

## Base URL

- Development: `http://localhost:8000`
- Production: Configurable via environment

## Endpoints

### GET /api/tasks

List all tasks for the authenticated user.

**Query Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| status | string | No | "all" | Filter: "all", "active", "completed" |
| priority | string | No | null | Filter: "high", "medium", "low" |
| category | string | No | null | Filter: "work", "home", "personal", "health", "other" |
| search | string | No | null | Search title and description |
| sort_by | string | No | "created_at" | Sort field: "created_at", "due_date", "title", "priority" |
| sort_order | string | No | "desc" | Sort direction: "asc", "desc" |

**Response 200**:
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "is_completed": false,
    "priority": "medium",
    "category": "home",
    "due_date": "2026-03-05",
    "recurrence": null,
    "due_time": "14:30",
    "reminder_minutes": 15,
    "reminder_sent": false,
    "created_at": "2026-03-02T10:00:00Z",
    "updated_at": "2026-03-02T10:00:00Z"
  }
]
```

**Response 401**: `{"detail": "Not authenticated"}`

---

### POST /api/tasks

Create a new task for the authenticated user.

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "medium",
  "category": "home",
  "due_date": "2026-03-05",
  "recurrence": "weekly",
  "due_time": "14:30",
  "reminder_minutes": 15
}
```

| Field | Type | Required | Default |
|-------|------|----------|---------|
| title | string | Yes | — |
| description | string | No | null |
| priority | string | No | "medium" |
| category | string | No | null |
| due_date | string (YYYY-MM-DD) | No | null |
| recurrence | string | No | null |
| due_time | string (HH:MM) | No | null |
| reminder_minutes | integer | No | null |

**Response 201**: Created task object (same schema as GET response item)
**Response 401**: `{"detail": "Not authenticated"}`
**Response 422**: `{"detail": [{"msg": "Title cannot be empty", ...}]}`

---

### GET /api/tasks/{task_id}

Get a single task by ID (must belong to authenticated user).

**Response 200**: Task object
**Response 401**: `{"detail": "Not authenticated"}`
**Response 404**: `{"detail": "Task not found"}`

---

### PUT /api/tasks/{task_id}

Update a task (must belong to authenticated user).

**Request Body**: Same fields as POST (title required, others optional).

**Response 200**: Updated task object
**Response 401**: `{"detail": "Not authenticated"}`
**Response 404**: `{"detail": "Task not found"}`
**Response 422**: Validation errors

---

### DELETE /api/tasks/{task_id}

Delete a task (must belong to authenticated user).

**Response 204**: No content
**Response 401**: `{"detail": "Not authenticated"}`
**Response 404**: `{"detail": "Task not found"}`

---

### PATCH /api/tasks/{task_id}/complete

Toggle task completion status. If completing a recurring task with a due_date, automatically creates the next occurrence.

**Response 200**: Updated task object (with new `is_completed` value)
**Response 401**: `{"detail": "Not authenticated"}`
**Response 404**: `{"detail": "Task not found"}`

## Error Response Format

All errors follow FastAPI's standard format:
```json
{
  "detail": "Error message string"
}
```

Or for validation errors (422):
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "Title cannot be empty",
      "type": "value_error"
    }
  ]
}
```

## CORS

Backend must allow requests from the frontend origin:
- Development: `http://localhost:3000`
- Production: Configurable via `FRONTEND_URL` environment variable
