from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from src.repository.database import get_session
from src.repository.task_repo import TaskRepository
from src.services.task_service import TaskService
from src.auth import get_current_user_id
from src.models.task import Task, PriorityEnum, CategoryEnum, RecurrenceEnum
from datetime import date
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

def get_task_service(session: Session = Depends(get_session)) -> TaskService:
    repo = TaskRepository(session)
    return TaskService(repo)

@router.get("/tasks", response_model=List[Task])
def list_tasks(
    status: str = Query("all", pattern="^(all|active|completed)$"),
    priority: Optional[PriorityEnum] = None,
    category: Optional[CategoryEnum] = None,
    search: Optional[str] = None,
    sort_by: str = Query("created_at", pattern="^(created_at|due_date|title|priority)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    user_id: str = Depends(get_current_user_id),
    service: TaskService = Depends(get_task_service),
):
    return service.list_tasks(
        user_id=user_id,
        status=status,
        priority=priority,
        category=category,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )

@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: dict,
    user_id: str = Depends(get_current_user_id),
    service: TaskService = Depends(get_task_service),
):
    try:
        return service.create_task(user_id, task_data)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/tasks/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    service: TaskService = Depends(get_task_service),
):
    task = service.get_task(user_id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_data: dict,
    user_id: str = Depends(get_current_user_id),
    service: TaskService = Depends(get_task_service),
):
    task = service.update_task(user_id, task_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    service: TaskService = Depends(get_task_service),
):
    if not service.delete_task(user_id, task_id):
        raise HTTPException(status_code=404, detail="Task not found")

@router.patch("/tasks/{task_id}/complete", response_model=Task)
def toggle_complete(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    service: TaskService = Depends(get_task_service),
):
    task = service.toggle_complete(user_id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task