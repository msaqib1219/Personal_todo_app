"""TaskService: validation + business logic."""

import re
from datetime import date

from dateutil.relativedelta import relativedelta

from src.config import logger
from src.models.task import VALID_CATEGORIES, VALID_PRIORITIES, VALID_RECURRENCES, Task
from src.repository.task_repo import TaskRepository

_TIME_RE = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")


class TaskService:
    """Business logic and validation. Delegates to TaskRepository."""

    def __init__(self, repo: TaskRepository):
        self._repo = repo

    def _validate_title(self, title: str) -> str:
        title = title.strip()
        if not title:
            raise ValueError("Title cannot be empty or whitespace-only")
        if len(title) > 500:
            raise ValueError("Title cannot exceed 500 characters")
        return title

    def _validate_priority(self, priority: str) -> str:
        if priority not in VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of: {', '.join(VALID_PRIORITIES)}")
        return priority

    def _validate_category(self, category: str | None) -> str | None:
        if category is not None and category not in VALID_CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(VALID_CATEGORIES)}")
        return category

    def _validate_recurrence(self, recurrence: str | None) -> str | None:
        if recurrence is not None and recurrence not in VALID_RECURRENCES:
            raise ValueError(f"Recurrence must be one of: {', '.join(VALID_RECURRENCES)}")
        return recurrence

    def _validate_due_time(self, due_time: str | None) -> str | None:
        if due_time is not None and not _TIME_RE.match(due_time):
            raise ValueError("Due time must be in HH:MM format (00:00–23:59)")
        return due_time

    def _validate_reminder_minutes(self, reminder_minutes: int | None) -> int | None:
        if reminder_minutes is not None and reminder_minutes < 0:
            raise ValueError("Reminder minutes cannot be negative")
        return reminder_minutes

    @staticmethod
    def _advance_date(current: date, recurrence: str) -> date:
        """Advance a date by the recurrence interval."""
        deltas = {
            "daily": relativedelta(days=1),
            "weekly": relativedelta(weeks=1),
            "monthly": relativedelta(months=1),
            "yearly": relativedelta(years=1),
        }
        return current + deltas[recurrence]

    def list_tasks(
        self,
        *,
        search: str | None = None,
        status: str | None = None,
        priority: str | None = None,
        category: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> list[Task]:
        return self._repo.get_all(
            search=search,
            status=status,
            priority=priority,
            category=category,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    def add_task(
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
        title = self._validate_title(title)
        priority = self._validate_priority(priority)
        category = self._validate_category(category)
        recurrence = self._validate_recurrence(recurrence)
        due_time = self._validate_due_time(due_time)
        reminder_minutes = self._validate_reminder_minutes(reminder_minutes)
        task = self._repo.create(
            title=title,
            description=description,
            priority=priority,
            category=category,
            due_date=due_date,
            recurrence=recurrence,
            due_time=due_time,
            reminder_minutes=reminder_minutes,
        )
        logger.info("Task created: id=%s title='%s'", task.id, task.title)
        return task

    def update_task(
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
    ) -> Task:
        title = self._validate_title(title)
        if priority is not None:
            priority = self._validate_priority(priority)
        category = self._validate_category(category)
        recurrence = self._validate_recurrence(recurrence)
        due_time = self._validate_due_time(due_time)
        reminder_minutes = self._validate_reminder_minutes(reminder_minutes)
        task = self._repo.update(
            task_id,
            title=title,
            description=description,
            priority=priority,
            category=category,
            due_date=due_date,
            recurrence=recurrence,
            due_time=due_time,
            reminder_minutes=reminder_minutes,
        )
        if task is None:
            raise KeyError(f"Task {task_id} not found")
        logger.info("Task updated: id=%s title='%s'", task.id, task.title)
        return task

    def toggle_task(self, task_id: int) -> Task:
        task = self._repo.toggle_completed(task_id)
        if task is None:
            raise KeyError(f"Task {task_id} not found")
        logger.info("Task toggled: id=%s completed=%s", task.id, task.is_completed)
        # If completing a recurring task with a due_date, create next occurrence
        if task.is_completed and task.recurrence and task.due_date:
            next_date = self._advance_date(task.due_date, task.recurrence)
            self._repo.create(
                title=task.title,
                description=task.description,
                priority=task.priority,
                category=task.category,
                due_date=next_date,
                recurrence=task.recurrence,
                due_time=task.due_time,
                reminder_minutes=task.reminder_minutes,
            )
            logger.info(
                "Recurring task created: next due_date=%s recurrence=%s",
                next_date, task.recurrence,
            )
        return task

    def delete_task(self, task_id: int) -> None:
        deleted = self._repo.delete(task_id)
        if not deleted:
            raise KeyError(f"Task {task_id} not found")
        logger.info("Task deleted: id=%s", task_id)
