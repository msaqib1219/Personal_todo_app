# Data Model: Personal Todo APP

**Date**: 2026-02-22
**Feature**: 001-todo-app

## Entities

### Task

The single entity in the system. Represents one todo item.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | Integer | Primary key, auto-increment | Unique identifier |
| title | String(500) | NOT NULL, 1-500 chars, no whitespace-only | Required; validated before write |
| description | Text | Nullable | Optional free-form text |
| is_completed | Boolean | NOT NULL, default=False | Completion toggle state |
| created_at | DateTime | NOT NULL, default=now() | Set on creation, immutable |
| updated_at | DateTime | NOT NULL, default=now(), on_update=now() | Auto-updated on any change |

### Validation Rules

- `title` MUST be stripped of leading/trailing whitespace before validation.
- `title` MUST be between 1 and 500 characters after stripping.
- `title` consisting only of whitespace MUST be rejected.
- `description` has no length limit (free text).
- `is_completed` can only be `True` or `False`.

### State Transitions

```text
[Created] ──── is_completed=False (default)
    │
    ▼
[Completed] ── is_completed=True (user toggles)
    │
    ▼
[Incomplete] ─ is_completed=False (user un-toggles)
    │
    ▼
[Deleted] ──── Row removed from database (permanent)
```

- Toggle: `is_completed` flips between True/False.
- Delete: Row is permanently removed (no soft-delete).
- Update: `title` and/or `description` can be modified at any state.

### Query Patterns

| Operation | Query | Ordering |
|-----------|-------|----------|
| List all tasks | SELECT * FROM tasks | ORDER BY created_at DESC (newest first) |
| Get single task | SELECT * FROM tasks WHERE id = ? | N/A |
| Create task | INSERT INTO tasks (title, description) | N/A |
| Update task | UPDATE tasks SET title=?, description=?, updated_at=now() WHERE id = ? | N/A |
| Toggle completion | UPDATE tasks SET is_completed=NOT is_completed, updated_at=now() WHERE id = ? | N/A |
| Delete task | DELETE FROM tasks WHERE id = ? | N/A |

### Storage

- **Engine**: SQLite (single local file)
- **Location**: `~/.todo-app/tasks.db` (platform-appropriate user data directory)
- **Volume**: Up to 500 tasks; all loaded into memory at startup
- **Migrations**: For v1.0.0, single table creation on first run.
  Future schema changes via Alembic or manual migration scripts.
