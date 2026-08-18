# Data Model: Full-Stack Web Application (Phase II)

**Feature**: 002-fullstack-web
**Date**: 2026-03-02

## Entities

### User (managed by Better Auth)

Better Auth automatically creates and manages these tables. The backend does NOT write to them directly.

| Field | Type | Constraints |
|-------|------|-------------|
| id | string | Primary key (UUID/CUID) |
| name | string | Required |
| email | string | Unique, required |
| emailVerified | boolean | Default false |
| image | string | Nullable |
| createdAt | timestamp | Auto-generated |
| updatedAt | timestamp | Auto-updated |

Additional Better Auth tables: `session`, `account`, `verification` — managed internally.

### Task (managed by backend)

Extended from Phase I with `user_id` field for multi-user support.

| Field | Type | Constraints |
|-------|------|-------------|
| id | integer | Primary key, auto-increment |
| user_id | string | Foreign key → user.id, required, indexed |
| title | string | Required, 1-500 chars |
| description | string | Nullable |
| is_completed | boolean | Default false |
| priority | string | Default "medium", enum: high/medium/low |
| category | string | Nullable, enum: work/home/personal/health/other |
| due_date | date | Nullable |
| recurrence | string | Nullable, enum: daily/weekly/monthly/yearly |
| due_time | string | Nullable, HH:MM format |
| reminder_minutes | integer | Nullable, non-negative |
| reminder_sent | boolean | Default false |
| created_at | timestamp | Auto-generated |
| updated_at | timestamp | Auto-updated |

### Indexes

- `tasks.user_id` — All queries filter by user
- `tasks.user_id + is_completed` — Status filtering
- `tasks.user_id + priority` — Priority filtering
- `tasks.user_id + category` — Category filtering

## Relationships

```
User (1) ──── (many) Task
  │                    │
  └── id ◄──── user_id ┘
```

## State Transitions

### Task Completion
```
incomplete ──toggle──► completed
completed  ──toggle──► incomplete

If completing + has recurrence + has due_date:
  → New Task created with advanced due_date
```

## Changes from Phase I

| Aspect | Phase I | Phase II |
|--------|---------|----------|
| Database | SQLite (local file) | Neon PostgreSQL (cloud) |
| User model | None (single user) | Better Auth managed |
| Task.user_id | Not present | Required foreign key |
| All queries | Global | Scoped by user_id |
| Connection | File path | Connection string + pooler |
