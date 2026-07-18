import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import date
from fastapi.testclient import TestClient
from src.main import app
from src.models.task import Task, PriorityEnum, CategoryEnum, RecurrenceEnum


client = TestClient(app)


class TestTaskEndpoints:
    @pytest.fixture
    def mock_user_id(self):
        return "user-123"

    @pytest.fixture
    def valid_token(self):
        return "Bearer valid.jwt.token"

    @pytest.fixture
    def mock_auth(self, mock_user_id):
        with patch("src.api.tasks.get_current_user_id") as mock:
            mock.return_value = mock_user_id
            yield mock

    def test_get_tasks_requires_auth(self):
        response = client.get("/api/tasks")
        assert response.status_code == 401

    def test_get_tasks_with_auth(self, mock_auth, mock_user_id):
        with patch("src.api.tasks.TaskService") as mock_service_class:
            mock_service = Mock()
            mock_service.list_tasks.return_value = [
                Task(
                    id=1,
                    user_id=mock_user_id,
                    title="Test task",
                    priority=PriorityEnum.medium,
                    is_completed=False,
                )
            ]
            mock_service_class.return_value = mock_service

            response = client.get("/api/tasks", headers={"Authorization": "Bearer token"})

        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_create_task_requires_auth(self):
        response = client.post("/api/tasks", json={"title": "Test"})
        assert response.status_code == 401

    def test_create_task_with_auth(self, mock_auth, mock_user_id):
        with patch("src.api.tasks.TaskService") as mock_service_class:
            mock_service = Mock()
            mock_service.create_task.return_value = Task(
                id=1,
                user_id=mock_user_id,
                title="Test task",
                priority=PriorityEnum.medium,
                is_completed=False,
            )
            mock_service_class.return_value = mock_service

            response = client.post(
                "/api/tasks",
                json={"title": "Test task", "priority": "high"},
                headers={"Authorization": "Bearer token"},
            )

        assert response.status_code == 201
        assert response.json()["title"] == "Test task"

    def test_get_task_not_found(self, mock_auth):
        with patch("src.api.tasks.TaskService") as mock_service_class:
            mock_service = Mock()
            mock_service.get_task.return_value = None
            mock_service_class.return_value = mock_service

            response = client.get("/api/tasks/999", headers={"Authorization": "Bearer token"})

        assert response.status_code == 404

    def test_update_task_not_found(self, mock_auth):
        with patch("src.api.tasks.TaskService") as mock_service_class:
            mock_service = Mock()
            mock_service.update_task.return_value = None
            mock_service_class.return_value = mock_service

            response = client.put(
                "/api/tasks/999",
                json={"title": "Updated"},
                headers={"Authorization": "Bearer token"},
            )

        assert response.status_code == 404

    def test_delete_task_success(self, mock_auth):
        with patch("src.api.tasks.TaskService") as mock_service_class:
            mock_service = Mock()
            mock_service.delete_task.return_value = True
            mock_service_class.return_value = mock_service

            response = client.delete(
                "/api/tasks/1",
                headers={"Authorization": "Bearer token"},
            )

        assert response.status_code == 204

    def test_delete_task_not_found(self, mock_auth):
        with patch("src.api.tasks.TaskService") as mock_service_class:
            mock_service = Mock()
            mock_service.delete_task.return_value = False
            mock_service_class.return_value = mock_service

            response = client.delete(
                "/api/tasks/999",
                headers={"Authorization": "Bearer token"},
            )

        assert response.status_code == 404

    def test_toggle_completion(self, mock_auth, mock_user_id):
        with patch("src.api.tasks.TaskService") as mock_service_class:
            mock_service = Mock()
            mock_service.toggle_completion.return_value = Task(
                id=1,
                user_id=mock_user_id,
                title="Test",
                priority=PriorityEnum.medium,
                is_completed=True,
            )
            mock_service_class.return_value = mock_service

            response = client.patch(
                "/api/tasks/1/complete",
                headers={"Authorization": "Bearer token"},
            )

        assert response.status_code == 200
        assert response.json()["is_completed"] is True