"""Integration tests for TaskRepository."""

from datetime import date


class TestTaskRepositoryCreate:
    def test_create_task(self, repo):
        task = repo.create(title="Test Task", description="Description")
        assert task.id is not None
        assert task.title == "Test Task"
        assert task.description == "Description"
        assert task.is_completed is False

    def test_create_task_without_description(self, repo):
        task = repo.create(title="No Desc")
        assert task.description is None

    def test_create_with_priority(self, repo):
        task = repo.create(title="High", priority="high")
        assert task.priority == "high"

    def test_create_with_category(self, repo):
        task = repo.create(title="Work", category="work")
        assert task.category == "work"

    def test_create_with_due_date(self, repo):
        d = date(2026, 12, 25)
        task = repo.create(title="Deadline", due_date=d)
        assert task.due_date == d


class TestTaskRepositoryCreateAdvanced:
    def test_create_with_recurrence(self, repo):
        task = repo.create(title="Recurring", recurrence="daily")
        assert task.recurrence == "daily"

    def test_create_with_due_time(self, repo):
        task = repo.create(title="Timed", due_time="14:30")
        assert task.due_time == "14:30"

    def test_create_with_reminder_minutes(self, repo):
        task = repo.create(title="Remind", reminder_minutes=10)
        assert task.reminder_minutes == 10

    def test_create_with_all_new_fields(self, repo):
        task = repo.create(
            title="Full",
            due_date=date(2026, 6, 1),
            recurrence="weekly",
            due_time="09:00",
            reminder_minutes=15,
        )
        assert task.recurrence == "weekly"
        assert task.due_time == "09:00"
        assert task.reminder_minutes == 15
        assert task.reminder_sent is False


class TestTaskRepositoryUpdateAdvanced:
    def test_update_recurrence(self, repo, sample_task):
        updated = repo.update(sample_task.id, title="Task", recurrence="monthly")
        assert updated.recurrence == "monthly"

    def test_update_due_time(self, repo, sample_task):
        updated = repo.update(sample_task.id, title="Task", due_time="16:00")
        assert updated.due_time == "16:00"

    def test_update_reminder_minutes(self, repo, sample_task):
        updated = repo.update(sample_task.id, title="Task", reminder_minutes=5)
        assert updated.reminder_minutes == 5

    def test_update_due_time_resets_reminder_sent(self, repo):
        task = repo.create(title="T", due_time="10:00", reminder_minutes=5)
        # Manually set reminder_sent
        task.reminder_sent = True
        repo._session.add(task)
        repo._session.commit()
        repo._session.refresh(task)
        assert task.reminder_sent is True
        # Update due_time → should reset
        updated = repo.update(task.id, title="T", due_time="11:00")
        assert updated.reminder_sent is False


class TestTaskRepositoryGetAll:
    def test_get_all_ordered_newest_first(self, repo):
        repo.create(title="First")
        repo.create(title="Second")
        repo.create(title="Third")
        tasks = repo.get_all()
        assert len(tasks) == 3
        assert tasks[0].title == "Third"
        assert tasks[2].title == "First"

    def test_get_all_empty(self, repo):
        assert repo.get_all() == []

    def test_filter_by_status_active(self, repo):
        repo.create(title="Active")
        t = repo.create(title="Done")
        repo.toggle_completed(t.id)
        tasks = repo.get_all(status="active")
        assert len(tasks) == 1
        assert tasks[0].title == "Active"

    def test_filter_by_priority(self, repo):
        repo.create(title="High", priority="high")
        repo.create(title="Low", priority="low")
        tasks = repo.get_all(priority="high")
        assert len(tasks) == 1
        assert tasks[0].title == "High"

    def test_filter_by_category(self, repo):
        repo.create(title="Work", category="work")
        repo.create(title="Home", category="home")
        tasks = repo.get_all(category="work")
        assert len(tasks) == 1
        assert tasks[0].title == "Work"

    def test_search_title(self, repo):
        repo.create(title="Buy groceries")
        repo.create(title="Read book")
        tasks = repo.get_all(search="groceries")
        assert len(tasks) == 1
        assert tasks[0].title == "Buy groceries"

    def test_sort_by_title_asc(self, repo):
        repo.create(title="Banana")
        repo.create(title="Apple")
        tasks = repo.get_all(sort_by="title", sort_order="asc")
        assert tasks[0].title == "Apple"

    def test_sort_by_priority(self, repo):
        repo.create(title="Low", priority="low")
        repo.create(title="High", priority="high")
        tasks = repo.get_all(sort_by="priority", sort_order="asc")
        assert tasks[0].priority == "high"
        assert tasks[1].priority == "low"


class TestTaskRepositoryGetById:
    def test_get_existing(self, repo, sample_task):
        found = repo.get_by_id(sample_task.id)
        assert found is not None
        assert found.id == sample_task.id

    def test_get_missing_returns_none(self, repo):
        assert repo.get_by_id(9999) is None


class TestTaskRepositoryUpdate:
    def test_update_task(self, repo, sample_task):
        updated = repo.update(sample_task.id, title="Updated", description="New desc")
        assert updated.title == "Updated"
        assert updated.description == "New desc"

    def test_update_missing_returns_none(self, repo):
        assert repo.update(9999, title="Nope") is None

    def test_update_priority(self, repo, sample_task):
        updated = repo.update(sample_task.id, title="Task", priority="high")
        assert updated.priority == "high"

    def test_update_category(self, repo, sample_task):
        updated = repo.update(sample_task.id, title="Task", category="home")
        assert updated.category == "home"

    def test_update_due_date(self, repo, sample_task):
        d = date(2026, 12, 25)
        updated = repo.update(sample_task.id, title="Task", due_date=d)
        assert updated.due_date == d


class TestTaskRepositoryToggle:
    def test_toggle_incomplete_to_complete(self, repo, sample_task):
        toggled = repo.toggle_completed(sample_task.id)
        assert toggled.is_completed is True

    def test_toggle_complete_to_incomplete(self, repo, sample_task):
        repo.toggle_completed(sample_task.id)
        toggled = repo.toggle_completed(sample_task.id)
        assert toggled.is_completed is False

    def test_toggle_missing_returns_none(self, repo):
        assert repo.toggle_completed(9999) is None


class TestTaskRepositoryDelete:
    def test_delete_task(self, repo, sample_task):
        assert repo.delete(sample_task.id) is True
        assert repo.get_by_id(sample_task.id) is None

    def test_delete_missing_returns_false(self, repo):
        assert repo.delete(9999) is False
