from sqlmodel import Field, SQLModel
from datetime import date, datetime
from typing import Optional
import enum

class PriorityEnum(str, enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"

class CategoryEnum(str, enum.Enum):
    work = "work"
    home = "home"
    personal = "personal"
    health = "health"
    other = "other"

class RecurrenceEnum(str, enum.Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    yearly = "yearly"

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=500)
    description: Optional[str] = Field(default=None)
    is_completed: bool = Field(default=False)
    priority: PriorityEnum = Field(default=PriorityEnum.medium)
    category: Optional[CategoryEnum] = Field(default=None)
    due_date: Optional[date] = Field(default=None)
    recurrence: Optional[RecurrenceEnum] = Field(default=None)
    due_time: Optional[str] = Field(default=None)
    reminder_minutes: Optional[int] = Field(default=None, ge=0)
    reminder_sent: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})