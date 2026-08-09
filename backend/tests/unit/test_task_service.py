import pytest
from datetime import date
from unittest.mock import Mock, MagicMock
from sqlmodel import Session
from src.models.task import Task, PriorityEnum, CategoryEnum, RecurrenceEnum
from src.services.task_service import TaskService
from src.repository.task_repo import TaskRepository, TaskFilters


@pytest.fixture
def mock_session():
    return Mock(spec=Session)


@pytest.fixture
def mock_repo():
    return Mock(spec=TaskRepository)


@pytest.fixture
def task_service(mock_repo):
    service = TaskService(Mock(spec=Session))
    service.repo = mock_repo
    return service


class TestTaskServiceValidation:
    def test_valid_task_data_passes(self, task_service):
        data = {"title": "Valid task", "priority": "high"}
        result = task_service.validate_task_data(data)
        assert result == data

    def test_empty_title_rejected(self, task_service):
        data = {"title": ""}
        with pytest.raises(ValueError, match="Title cannot be empty"):
            task_service.validate_task_data(data)

    def test_title_too_long_rejected(self, task_service):
        data = {"title": "a" * 501}
        with pytest.raises(ValueError, match="Title cannot exceed 500 characters"):
            task_service.validate_task_data(data)

    def test_invalid_priority_rejected(self, task_service):
        data = {"title": "Task", "priority": "urgent"}
        with pytest.raises(ValueError, match="Invalid priority"):
            task_service.validate_task_data(data)

    def test_invalid_category_rejected(self, task_service):
        data = {"title": "Task", "category": "invalid"}
        with pytest.raises(ValueError, match="Invalid category"):
            task_service.validate_task_data(data)

    def test_invalid_due_time_format_rejected(self, task_service):
        data = {"title": "Task", "due_time": "25:00"}
        with pytest.raises(ValueError, match="due_time must be in HH:MM format"):
            task_service.validate_task_data(data)

    def test_negative_reminder_minutes_rejected(self, task_service):
        data = {"title": "Task", "reminder_minutes": -5}
        with pytest.raises(ValueError, match="reminder_minutes must be a non-negative integer"):
            task_service.validate_task_data(data)

    def test_valid_input_accepted(self, task_service):
        data = {
            "title": "Valid task",
            "priority": "medium",
            "category": "work",
            "due_time": "14:30",
            "reminder_minutes": 15,
        }
        result = task_service.validate_task_data(data)
        assert result == data


class TestRecurrenceLogic:
    def test_daily_recurrence_adds_one_day(self, task_service):
        current = date(2026, 3, 5)
        next_date = task_service._calculate_next_due_date(current, RecurrenceEnum.daily)
        assert next_date == date(2026, 3, 6)

    def test_weekly_recurrence_adds_seven_days(self, task_service):
        current = date(2026, 3, 5)
        next_date = task_service._calculate_next_due_date(current, RecurrenceEnum.weekly)
        assert next_date == date(2026, 3, 12)

    def test_monthly_recurrence_adds_one_month(self, task_service):
        current = date(2026, 3, 5)
        next_date = task_service._calculate_next_due_date(current, RecurrenceEnum.monthly)
        assert next_date == date(2026, 4, 5)

    def test_yearly_recurrence_adds_one_year(self, task_service):
        current = date(2026, 3, 5)
        next_date = task_service._calculate_next_due_date(current, RecurrenceEnum.yearly)
        assert next_date == date(2027, 3, 5)

    def test_no_recurrence_returns_none(self, task_service):
        current = date(2026, 3, 5)
        next_date = task_service._calculate_next_due_date(current, None)
        assert next_date is None