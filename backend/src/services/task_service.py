from typing import Optional, List, Dict, Any
from datetime import date, datetime, timedelta
from sqlmodel import Session
from src.models.task import Task, PriorityEnum, CategoryEnum, RecurrenceEnum
from src.repository.task_repo import TaskRepository, TaskFilters
from src.repository.database import get_session
import re


class TaskService:
    VALID_PRIORITIES = {"high", "medium", "low"}
    VALID_CATEGORIES = {"work", "home", "personal", "health", "other"}
    VALID_RECURRENCES = {"daily", "weekly", "monthly", "yearly"}

    def __init__(self, session: Session):
        self.repo = TaskRepository(session)

    def validate_task_data(self, data: Dict[str, Any], is_update: bool = False) -> Dict[str, Any]:
        errors = []

        if "title" in data:
            title = data["title"]
            if not title or not title.strip():
                errors.append("Title cannot be empty")
            elif len(title) > 500:
                errors.append("Title cannot exceed 500 characters")

        if "priority" in data and data["priority"]:
            if data["priority"] not in self.VALID_PRIORITIES:
                errors.append(f"Invalid priority: must be one of {self.VALID_PRIORITIES}")

        if "category" in data and data["category"]:
            if data["category"] not in self.VALID_CATEGORIES:
                errors.append(f"Invalid category: must be one of {self.VALID_CATEGORIES}")

        if "due_time" in data and data["due_time"]:
            if not re.match(r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$", data["due_time"]):
                errors.append("due_time must be in HH:MM format")

        if "reminder_minutes" in data and data["reminder_minutes"] is not None:
            if not isinstance(data["reminder_minutes"], int) or data["reminder_minutes"] < 0:
                errors.append("reminder_minutes must be a non-negative integer")

        if "recurrence" in data and data["recurrence"]:
            if data["recurrence"] not in self.VALID_RECURRENCES:
                errors.append(f"Invalid recurrence: must be one of {self.VALID_RECURRENCES}")

        if errors:
            raise ValueError(", ".join(errors))

        return data

    def create_task(self, user_id: str, data: Dict[str, Any]) -> Task:
        validated = self.validate_task_data(data)
        task = Task(
            user_id=user_id,
            title=validated["title"],
            description=validated.get("description"),
            priority=PriorityEnum(validated.get("priority", "medium")),
            category=CategoryEnum(validated["category"]) if validated.get("category") else None,
            due_date=validated.get("due_date"),
            recurrence=RecurrenceEnum(validated["recurrence"]) if validated.get("recurrence") else None,
            due_time=validated.get("due_time"),
            reminder_minutes=validated.get("reminder_minutes"),
        )
        return self.repo.create(user_id, task)

    def get_task(self, user_id: str, task_id: int) -> Optional[Task]:
        return self.repo.get_by_id(user_id, task_id)

    def list_tasks(
        self,
        user_id: str,
        status: str = "all",
        priority: Optional[str] = None,
        category: Optional[str] = None,
        search: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> List[Task]:
        filters = TaskFilters(
            status=status,
            priority=priority,
            category=category,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        return self.repo.list(user_id, filters)

    def update_task(self, user_id: str, task_id: int, data: Dict[str, Any]) -> Optional[Task]:
        validated = self.validate_task_data(data, is_update=True)
        return self.repo.update(user_id, task_id, validated)

    def delete_task(self, user_id: str, task_id: int) -> bool:
        return self.repo.delete(user_id, task_id)

    def toggle_completion(self, user_id: str, task_id: int) -> Optional[Task]:
        task = self.get_task(user_id, task_id)
        if not task:
            return None

        new_status = not task.is_completed
        updated = self.repo.update(user_id, task_id, {"is_completed": new_status})

        if new_status and updated and updated.recurrence and updated.due_date:
            self._create_next_occurrence(user_id, updated)

        return updated

    def _create_next_occurrence(self, user_id: str, completed_task: Task) -> Optional[Task]:
        if not completed_task.recurrence or not completed_task.due_date:
            return None

        next_due_date = self._calculate_next_due_date(
            completed_task.due_date, completed_task.recurrence
        )
        if not next_due_date:
            return None

        new_task = Task(
            user_id=user_id,
            title=completed_task.title,
            description=completed_task.description,
            priority=completed_task.priority,
            category=completed_task.category,
            due_date=next_due_date,
            recurrence=completed_task.recurrence,
            due_time=completed_task.due_time,
            reminder_minutes=completed_task.reminder_minutes,
        )
        return self.repo.create(user_id, new_task)

    def _calculate_next_due_date(self, current_due_date: date, recurrence: RecurrenceEnum) -> Optional[date]:
        if recurrence == RecurrenceEnum.daily:
            return current_due_date + timedelta(days=1)
        elif recurrence == RecurrenceEnum.weekly:
            return current_due_date + timedelta(weeks=1)
        elif recurrence == RecurrenceEnum.monthly:
            month = current_due_date.month + 1
            year = current_due_date.year + (month // 13)
            month = month % 13 or 12
            day = min(current_due_date.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
            return date(year, month, day)
        elif recurrence == RecurrenceEnum.yearly:
            return current_due_date.replace(year=current_due_date.year + 1)
        return None