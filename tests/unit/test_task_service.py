"""Unit tests for TaskService."""

from datetime import date

import pytest
from sqlmodel import Session, SQLModel, create_engine

from src.repository.task_repo import TaskRepository
from src.services.task_service import TaskService


@pytest.fixture
def service():
    engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    repo = TaskRepository(session)
    return TaskService(repo)


class TestAddTask:
    def test_valid_title_creates_task(self, service):
        task = service.add_task("My Task")
        assert task.title == "My Task"
        assert task.id is not None

    def test_empty_title_raises(self, service):
        with pytest.raises(ValueError):
            service.add_task("")

    def test_whitespace_only_raises(self, service):
        with pytest.raises(ValueError):
            service.add_task("   ")

    def test_title_too_long_raises(self, service):
        with pytest.raises(ValueError):
            service.add_task("x" * 501)

    def test_optional_description(self, service):
        task = service.add_task("Task", description="Some desc")
        assert task.description == "Some desc"

    def test_valid_priority(self, service):
        task = service.add_task("Task", priority="high")
        assert task.priority == "high"

    def test_invalid_priority_raises(self, service):
        with pytest.raises(ValueError, match="Priority must be one of"):
            service.add_task("Task", priority="urgent")

    def test_valid_category(self, service):
        task = service.add_task("Task", category="work")
        assert task.category == "work"

    def test_invalid_category_raises(self, service):
        with pytest.raises(ValueError, match="Category must be one of"):
            service.add_task("Task", category="invalid")

    def test_none_category_allowed(self, service):
        task = service.add_task("Task", category=None)
        assert task.category is None

    def test_due_date(self, service):
        d = date(2026, 12, 25)
        task = service.add_task("Task", due_date=d)
        assert task.due_date == d

    def test_default_priority_is_medium(self, service):
        task = service.add_task("Task")
        assert task.priority == "medium"


class TestListTasks:
    def test_returns_all_tasks(self, service):
        service.add_task("A")
        service.add_task("B")
        assert len(service.list_tasks()) == 2

    def test_ordered_newest_first(self, service):
        service.add_task("First")
        service.add_task("Second")
        tasks = service.list_tasks()
        assert tasks[0].title == "Second"

    def test_empty_list(self, service):
        assert service.list_tasks() == []

    def test_filter_by_status_active(self, service):
        service.add_task("Active")
        t = service.add_task("Done")
        service.toggle_task(t.id)
        tasks = service.list_tasks(status="active")
        assert len(tasks) == 1
        assert tasks[0].title == "Active"

    def test_filter_by_status_completed(self, service):
        service.add_task("Active")
        t = service.add_task("Done")
        service.toggle_task(t.id)
        tasks = service.list_tasks(status="completed")
        assert len(tasks) == 1
        assert tasks[0].title == "Done"

    def test_filter_by_priority(self, service):
        service.add_task("High", priority="high")
        service.add_task("Low", priority="low")
        tasks = service.list_tasks(priority="high")
        assert len(tasks) == 1
        assert tasks[0].title == "High"

    def test_filter_by_category(self, service):
        service.add_task("Work", category="work")
        service.add_task("Home", category="home")
        tasks = service.list_tasks(category="work")
        assert len(tasks) == 1
        assert tasks[0].title == "Work"

    def test_search_by_title(self, service):
        service.add_task("Buy groceries")
        service.add_task("Read book")
        tasks = service.list_tasks(search="groceries")
        assert len(tasks) == 1
        assert tasks[0].title == "Buy groceries"

    def test_sort_by_title_asc(self, service):
        service.add_task("Banana")
        service.add_task("Apple")
        tasks = service.list_tasks(sort_by="title", sort_order="asc")
        assert tasks[0].title == "Apple"
        assert tasks[1].title == "Banana"

    def test_sort_by_priority(self, service):
        service.add_task("Low", priority="low")
        service.add_task("High", priority="high")
        service.add_task("Med", priority="medium")
        tasks = service.list_tasks(sort_by="priority", sort_order="asc")
        assert tasks[0].priority == "high"
        assert tasks[2].priority == "low"


class TestToggleTask:
    def test_toggle_to_complete(self, service):
        task = service.add_task("Task")
        toggled = service.toggle_task(task.id)
        assert toggled.is_completed is True

    def test_toggle_to_incomplete(self, service):
        task = service.add_task("Task")
        service.toggle_task(task.id)
        toggled = service.toggle_task(task.id)
        assert toggled.is_completed is False

    def test_toggle_missing_raises(self, service):
        with pytest.raises(KeyError):
            service.toggle_task(9999)


class TestUpdateTask:
    def test_valid_update(self, service):
        task = service.add_task("Original")
        updated = service.update_task(task.id, "Updated", "New desc")
        assert updated.title == "Updated"
        assert updated.description == "New desc"

    def test_empty_title_raises(self, service):
        task = service.add_task("Original")
        with pytest.raises(ValueError):
            service.update_task(task.id, "")

    def test_missing_task_raises(self, service):
        with pytest.raises(KeyError):
            service.update_task(9999, "Nope")

    def test_updated_at_changes(self, service):
        task = service.add_task("Original")
        old_updated = task.updated_at
        updated = service.update_task(task.id, "Changed")
        assert updated.updated_at >= old_updated

    def test_update_with_priority(self, service):
        task = service.add_task("Task", priority="low")
        updated = service.update_task(task.id, "Task", priority="high")
        assert updated.priority == "high"

    def test_update_invalid_priority_raises(self, service):
        task = service.add_task("Task")
        with pytest.raises(ValueError):
            service.update_task(task.id, "Task", priority="urgent")

    def test_update_with_category(self, service):
        task = service.add_task("Task")
        updated = service.update_task(task.id, "Task", category="home")
        assert updated.category == "home"

    def test_update_with_due_date(self, service):
        task = service.add_task("Task")
        d = date(2026, 12, 25)
        updated = service.update_task(task.id, "Task", due_date=d)
        assert updated.due_date == d


class TestRecurrenceValidation:
    def test_valid_recurrences(self, service):
        for r in ("daily", "weekly", "monthly", "yearly"):
            task = service.add_task("Task", recurrence=r)
            assert task.recurrence == r

    def test_invalid_recurrence_raises(self, service):
        with pytest.raises(ValueError, match="Recurrence must be one of"):
            service.add_task("Task", recurrence="biweekly")

    def test_none_recurrence_allowed(self, service):
        task = service.add_task("Task", recurrence=None)
        assert task.recurrence is None


class TestDueTimeValidation:
    def test_valid_due_time(self, service):
        task = service.add_task("Task", due_time="14:30")
        assert task.due_time == "14:30"

    def test_invalid_hour_raises(self, service):
        with pytest.raises(ValueError, match="HH:MM"):
            service.add_task("Task", due_time="25:00")

    def test_invalid_format_raises(self, service):
        with pytest.raises(ValueError, match="HH:MM"):
            service.add_task("Task", due_time="2pm")

    def test_none_due_time_allowed(self, service):
        task = service.add_task("Task", due_time=None)
        assert task.due_time is None


class TestReminderMinutesValidation:
    def test_negative_raises(self, service):
        with pytest.raises(ValueError, match="negative"):
            service.add_task("Task", reminder_minutes=-5)

    def test_zero_allowed(self, service):
        task = service.add_task("Task", reminder_minutes=0)
        assert task.reminder_minutes == 0

    def test_positive_allowed(self, service):
        task = service.add_task("Task", reminder_minutes=30)
        assert task.reminder_minutes == 30


class TestToggleRecurrence:
    def test_toggle_creates_next_occurrence(self, service):
        from datetime import date
        task = service.add_task(
            "Daily task", due_date=date(2026, 3, 1), recurrence="daily"
        )
        service.toggle_task(task.id)
        tasks = service.list_tasks()
        assert len(tasks) == 2
        new_task = [t for t in tasks if not t.is_completed][0]
        assert new_task.due_date == date(2026, 3, 2)
        assert new_task.recurrence == "daily"

    def test_toggle_no_recurrence_no_new_task(self, service):
        task = service.add_task("Plain task")
        service.toggle_task(task.id)
        assert len(service.list_tasks()) == 1

    def test_toggle_recurring_no_due_date_no_new_task(self, service):
        task = service.add_task("Recurring no date", recurrence="weekly")
        service.toggle_task(task.id)
        assert len(service.list_tasks()) == 1

    def test_monthly_edge_case_jan31(self, service):
        from datetime import date
        task = service.add_task(
            "Monthly", due_date=date(2026, 1, 31), recurrence="monthly"
        )
        service.toggle_task(task.id)
        tasks = service.list_tasks()
        new_task = [t for t in tasks if not t.is_completed][0]
        assert new_task.due_date == date(2026, 2, 28)

    def test_uncomplete_does_not_create_new(self, service):
        from datetime import date
        task = service.add_task(
            "Daily", due_date=date(2026, 3, 1), recurrence="daily"
        )
        service.toggle_task(task.id)  # complete → creates new
        service.toggle_task(task.id)  # uncomplete → no new task
        assert len(service.list_tasks()) == 2


class TestDeleteTask:
    def test_delete_removes_task(self, service):
        task = service.add_task("Doomed")
        service.delete_task(task.id)
        assert len(service.list_tasks()) == 0

    def test_delete_missing_raises(self, service):
        with pytest.raises(KeyError):
            service.delete_task(9999)
