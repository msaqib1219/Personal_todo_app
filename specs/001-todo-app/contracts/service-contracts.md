# Service Contracts: Personal Todo APP

**Date**: 2026-02-22
**Feature**: 001-todo-app

> Note: This is a desktop GUI app with no HTTP API. Contracts are
> defined as internal Python service interfaces (method signatures)
> that the GUI layer calls.

## TaskRepository (data access layer)

```python
class TaskRepository:
    """Direct database access. No business logic."""

    def get_all(self) -> list[Task]:
        """Return all tasks ordered by created_at DESC."""

    def get_by_id(self, task_id: int) -> Task | None:
        """Return a single task or None if not found."""

    def create(self, title: str, description: str | None) -> Task:
        """Insert a new task. Returns the created Task."""

    def update(self, task_id: int, title: str,
               description: str | None) -> Task | None:
        """Update title/description. Returns updated Task or None."""

    def toggle_completed(self, task_id: int) -> Task | None:
        """Flip is_completed. Returns updated Task or None."""

    def delete(self, task_id: int) -> bool:
        """Delete a task. Returns True if deleted, False if not found."""
```

## TaskService (business logic layer)

```python
class TaskService:
    """Business logic and validation. Delegates to TaskRepository."""

    def list_tasks(self) -> list[Task]:
        """Get all tasks (newest first)."""

    def add_task(self, title: str,
                 description: str | None = None) -> Task:
        """Validate and create a new task.
        Raises ValueError if title is empty/whitespace-only
        or exceeds 500 characters."""

    def update_task(self, task_id: int, title: str,
                    description: str | None = None) -> Task:
        """Validate and update a task.
        Raises ValueError if title is invalid.
        Raises KeyError if task_id not found."""

    def toggle_task(self, task_id: int) -> Task:
        """Toggle completion status.
        Raises KeyError if task_id not found."""

    def delete_task(self, task_id: int) -> None:
        """Delete a task.
        Raises KeyError if task_id not found."""
```

## Error Taxonomy

| Error | Raised By | When |
|-------|-----------|------|
| `ValueError` | TaskService | Title validation fails (empty, whitespace, >500 chars) |
| `KeyError` | TaskService | Task ID not found for update/toggle/delete |
| `sqlite3.DatabaseError` | TaskRepository | Database file corrupted or inaccessible |

## GUI ↔ Service Contract

The GUI layer calls `TaskService` methods and handles:
- `ValueError` → Show validation error message in the GUI
- `KeyError` → Show "Task not found" error (edge case)
- `sqlite3.DatabaseError` → Show "Database error" warning, create fresh DB
