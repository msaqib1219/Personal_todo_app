"""Task SQLModel entity."""

from datetime import date, datetime

from sqlmodel import Field, SQLModel

VALID_PRIORITIES = ("high", "medium", "low")
VALID_CATEGORIES = ("work", "home", "personal", "health", "other")
VALID_RECURRENCES = ("daily", "weekly", "monthly", "yearly")
DEFAULT_REMINDER_MINUTES = 15


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=500)
    description: str | None = Field(default=None)
    is_completed: bool = Field(default=False)
    priority: str = Field(default="medium")
    category: str | None = Field(default=None)
    due_date: date | None = Field(default=None)
    recurrence: str | None = Field(default=None)
    due_time: str | None = Field(default=None)
    reminder_minutes: int | None = Field(default=None)
    reminder_sent: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
