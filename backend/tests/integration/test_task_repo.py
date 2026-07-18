import pytest
from unittest.mock import Mock, MagicMock
from datetime import date
from src.repository.task_repo import TaskRepository, TaskFilters
from src.models.task import Task, PriorityEnum, CategoryEnum, RecurrenceEnum


class TestTaskRepository:
    @pytest.fixture
    def mock_session(self):
        return Mock()

    @pytest.fixture
    def repo(self, mock_session):
        return TaskRepository(mock_session)

    def test_create_task(self, repo, mock_session):
        task = Task(
            user_id="user-123",
            title="Test task",
            priority=PriorityEnum.medium,
        )
        mock_session.add = Mock()
        mock_session.flush = Mock()
        mock_session.refresh = Mock()

        result = repo.create("user-123", task)

        assert result.user_id == "user-123"
        assert result.title == "Test task"
        mock_session.add.assert_called_once_with(task)
        mock_session.flush.assert_called_once()
        mock_session.refresh.assert_called_once_with(task)

    def test_get_by_id_own_task(self, repo, mock_session):
        task = Task(id=1, user_id="user-123", title="Test")
        mock_session.exec = Mock(return_value=Mock(first=Mock(return_value=task)))

        result = repo.get_by_id("user-123", 1)

        assert result == task
        mock_session.exec.assert_called_once()

    def test_get_by_id_other_user_returns_none(self, repo, mock_session):
        mock_session.exec = Mock(return_value=Mock(first=Mock(return_value=None)))

        result = repo.get_by_id("user-123", 999)

        assert result is None

    def test_list_tasks_with_filters(self, repo, mock_session):
        tasks = [
            Task(id=1, user_id="user-123", title="Task 1", priority=PriorityEnum.high),
            Task(id=2, user_id="user-123", title="Task 2", priority=PriorityEnum.low),
        ]
        mock_session.exec = Mock(return_value=Mock(all=Mock(return_value=tasks)))

        filters = TaskFilters(
            status="active",
            priority="high",
            category=None,
            search="test",
            sort_by="created_at",
            sort_order="desc",
        )
        result = repo.list("user-123", filters)

        assert len(result) == 2
        mock_session.exec.assert_called_once()

    def test_update_task(self, repo, mock_session):
        task = Task(id=1, user_id="user-123", title="Old", priority=PriorityEnum.medium)
        mock_session.exec = Mock(return_value=Mock(first=Mock(return_value=task)))
        mock_session.add = Mock()
        mock_session.flush = Mock()
        mock_session.refresh = Mock()

        result = repo.update("user-123", 1, {"title": "New", "priority": "high"})

        assert result.title == "New"
        assert result.priority == "high"
        mock_session.add.assert_called_once_with(task)
        mock_session.flush.assert_called_once()
        mock_session.refresh.assert_called_once_with(task)

    def test_delete_task_success(self, repo, mock_session):
        task = Task(id=1, user_id="user-123", title="Test")
        mock_session.exec = Mock(return_value=Mock(first=Mock(return_value=task)))
        mock_session.delete = Mock()
        mock_session.flush = Mock()

        result = repo.delete("user-123", 1)

        assert result is True
        mock_session.delete.assert_called_once_with(task)
        mock_session.flush.assert_called_once()

    def test_delete_task_not_found(self, repo, mock_session):
        mock_session.exec = Mock(return_value=Mock(first=Mock(return_value=None)))

        result = repo.delete("user-123", 999)

        assert result is False