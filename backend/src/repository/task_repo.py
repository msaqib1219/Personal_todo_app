from sqlmodel import Session, select, col
from src.models.task import Task, PriorityEnum, CategoryEnum, RecurrenceEnum
from datetime import date
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user_id: str, task: Task) -> Task:
        task.user_id = user_id
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        logger.info(f"Created task {task.id} for user {user_id}")
        return task

    def get_by_id(self, user_id: str, task_id: int) -> Optional[Task]:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        return self.session.exec(statement).first()

    def list(
        self,
        user_id: str,
        status: Optional[str] = None,
        priority: Optional[PriorityEnum] = None,
        category: Optional[CategoryEnum] = None,
        search: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> List[Task]:
        statement = select(Task).where(Task.user_id == user_id)

        if status == "active":
            statement = statement.where(Task.is_completed == False)
        elif status == "completed":
            statement = statement.where(Task.is_completed == True)

        if priority:
            statement = statement.where(Task.priority == priority)
        if category:
            statement = statement.where(Task.category == category)
        if search:
            search_term = f"%{search}%"
            statement = statement.where(
                Task.title.ilike(search_term) | Task.description.ilike(search_term)
            )

        sort_column = getattr(Task, sort_by, Task.created_at)
        if sort_order == "asc":
            statement = statement.order_by(sort_column.asc())
        else:
            statement = statement.order_by(sort_column.desc())

        return list(self.session.exec(statement).all())

    def update(self, user_id: str, task_id: int, data: dict) -> Optional[Task]:
        task = self.get_by_id(user_id, task_id)
        if not task:
            return None

        for key, value in data.items():
            if hasattr(task, key) and key not in ("id", "user_id", "created_at"):
                setattr(task, key, value)

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        logger.info(f"Updated task {task_id} for user {user_id}")
        return task

    def delete(self, user_id: str, task_id: int) -> bool:
        task = self.get_by_id(user_id, task_id)
        if not task:
            return False

        self.session.delete(task)
        self.session.commit()
        logger.info(f"Deleted task {task_id} for user {user_id}")
        return True