import pytest
import responses

from tools.directory import get_departments, get_operators


class TestGetDepartments:
    @pytest.mark.unit
    @responses.activate
    def test_get_departments_success(self):
        # Arrange
        departments_data = {
            "departments": [
                {"id": "535eb95e-107c-440a-8720-53649368a26a", "name": "Finances"},
                {"id": "7f14e5f9-1df0-439d-9b39-bd7e1e82fac5", "name": "Sales"},
            ]
        }
        responses.add(
            responses.GET,
            "https://api.tidio.com/departments",
            json=departments_data,
            status=200,
        )

        # Act
        result = get_departments()

        # Assert
        assert result == {"status": "ok", "data": departments_data}

    @pytest.mark.unit
    @responses.activate
    def test_get_departments_empty_response(self):
        # Arrange
        departments_data = {"departments": []}
        responses.add(
            responses.GET,
            "https://api.tidio.com/departments",
            json=departments_data,
            status=200,
        )

        # Act
        result = get_departments()

        # Assert
        assert result == {"status": "ok", "data": departments_data}


class TestGetOperators:
    @pytest.mark.unit
    @responses.activate
    def test_get_operators_success(self):
        # Arrange
        operators_data = {
            "operators": [
                {
                    "id": "fe7df646-6881-4d44-bcd5-639501a32bfe",
                    "active": True,
                    "email": "john.smith@company.com",
                    "name": "John Smith",
                    "role": "owner",
                    "picture": "https://example.com/avatars/john.jpg",
                    "last_seen": "2025-09-06T14:29:31+00:00",
                },
                {
                    "id": "dc017931-764b-4921-a8d6-bd967e91c955",
                    "active": False,
                    "email": "jane.doe@company.com",
                    "name": None,
                    "role": "chat_agent",
                    "picture": None,
                    "last_seen": None,
                },
            ],
            "meta": {
                "cursor": None,
                "limit": 100,
            },
        }
        responses.add(
            responses.GET,
            "https://api.tidio.com/operators",
            json=operators_data,
            status=200,
        )

        # Act
        result = get_operators()

        # Assert
        assert result == {"status": "ok", "data": operators_data}

    @pytest.mark.unit
    @responses.activate
    def test_get_operators_empty_response(self):
        # Arrange
        operators_data = {
            "operators": [],
            "meta": {
                "cursor": None,
                "limit": 100,
            },
        }
        responses.add(
            responses.GET,
            "https://api.tidio.com/operators",
            json=operators_data,
            status=200,
        )

        # Act
        result = get_operators()

        # Assert
        assert result == {"status": "ok", "data": operators_data}

    @pytest.mark.unit
    @responses.activate
    def test_get_operators_with_cursor(self):
        # Arrange
        cursor = "aWRfX2U2YTgyYTc0LTExNzAtNGY1Ny1hMDMxLWIzNmYzZjZiYzA5Mw=="
        operators_data = {
            "operators": [
                {
                    "id": "fe7df646-6881-4d44-bcd5-639501a32bfe",
                    "active": True,
                    "email": "john.smith@company.com",
                    "name": "John Smith",
                    "role": "owner",
                    "picture": "https://example.com/avatars/john.jpg",
                    "last_seen": "2025-09-06T14:29:31+00:00",
                },
            ],
            "meta": {
                "cursor": "next_cursor_value",
                "limit": 100,
            },
        }
        responses.add(
            responses.GET,
            f"https://api.tidio.com/operators?cursor={cursor}",
            json=operators_data,
            status=200,
        )

        # Act
        result = get_operators(cursor=cursor)

        # Assert
        assert result == {"status": "ok", "data": operators_data}
