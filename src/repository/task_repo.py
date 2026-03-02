"""TaskRepository: SQLite CRUD via SQLModel."""

from datetime import date, datetime

from sqlmodel import Session, select

from src.models.task import Task

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class TaskRepository:
    """Direct database access. No business logic."""

    def __init__(self, session: Session):
        self._session = session

    def get_all(
        self,
        *,
        search: str | None = None,
        status: str | None = None,
        priority: str | None = None,
        category: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> list[Task]:
        """Return tasks with optional filtering and sorting."""
        statement = select(Task)

        if search:
            statement = statement.where(
                Task.title.contains(search) | Task.description.contains(search)  # type: ignore[union-attr]
            )

        if status == "active":
            statement = statement.where(Task.is_completed == False)  # noqa: E712
        elif status == "completed":
            statement = statement.where(Task.is_completed == True)  # noqa: E712

        if priority:
            statement = statement.where(Task.priority == priority)

        if category:
            statement = statement.where(Task.category == category)

        # Sorting
        sort_column = {
            "created_at": Task.created_at,
            "due_date": Task.due_date,
            "title": Task.title,
            "priority": Task.priority,
        }.get(sort_by, Task.created_at)

        if sort_order == "asc":
            statement = statement.order_by(sort_column.asc())  # type: ignore[union-attr]
        else:
            statement = statement.order_by(sort_column.desc())  # type: ignore[union-attr]

        tasks = list(self._session.exec(statement).all())

        # Custom sort for priority since string ordering doesn't match semantic ordering
        if sort_by == "priority":
            tasks.sort(
                key=lambda t: PRIORITY_ORDER.get(t.priority, 1),
                reverse=(sort_order == "desc"),
            )

        return tasks

    def get_by_id(self, task_id: int) -> Task | None:
        """Return a single task or None if not found."""
        return self._session.get(Task, task_id)

    def create(
        self,
        title: str,
        description: str | None = None,
        priority: str = "medium",
        category: str | None = None,
        due_date: date | None = None,
        recurrence: str | None = None,
        due_time: str | None = None,
        reminder_minutes: int | None = None,
    ) -> Task:
        """Insert a new task. Returns the created Task."""
        task = Task(
            title=title,
            description=description,
            priority=priority,
            category=category,
            due_date=due_date,
            recurrence=recurrence,
            due_time=due_time,
            reminder_minutes=reminder_minutes,
        )
        self._session.add(task)
        self._session.commit()
        self._session.refresh(task)
        return task

    def update(
        self,
        task_id: int,
        title: str,
        description: str | None = None,
        priority: str | None = None,
        category: str | None = None,
        due_date: date | None = None,
        recurrence: str | None = None,
        due_time: str | None = None,
        reminder_minutes: int | None = None,
    ) -> Task | None:
        """Update task fields. Returns updated Task or None."""
        task = self.get_by_id(task_id)
        if task is None:
            return None
        # Reset reminder_sent if due_date or due_time changed
        if due_date != task.due_date or due_time != task.due_time:
            task.reminder_sent = False
        task.title = title
        task.description = description
        if priority is not None:
            task.priority = priority
        task.category = category
        task.due_date = due_date
        task.recurrence = recurrence
        task.due_time = due_time
        task.reminder_minutes = reminder_minutes
        task.updated_at = datetime.now()
        self._session.add(task)
        self._session.commit()
        self._session.refresh(task)
        return task

    def toggle_completed(self, task_id: int) -> Task | None:
        """Flip is_completed. Returns updated Task or None."""
        task = self.get_by_id(task_id)
        if task is None:
            return None
        task.is_completed = not task.is_completed
        task.updated_at = datetime.now()
        self._session.add(task)
        self._session.commit()
        self._session.refresh(task)
        return task

    def delete(self, task_id: int) -> bool:
        """Delete a task. Returns True if deleted, False if not found."""
        task = self.get_by_id(task_id)
        if task is None:
            return False
        self._session.delete(task)
        self._session.commit()
        return True
