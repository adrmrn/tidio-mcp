import json

import pytest
import requests
import responses

from tidio_client import TidioApiClient, TidioApiError


class TestTidioApiClient:
    TEST_CLIENT_ID = "test_client_id"
    TEST_CLIENT_SECRET = "test_client_secret"
    ACCEPT_HEADER = "application/json; version=1"

    def setup_method(self):
        self.sut = TidioApiClient(self.TEST_CLIENT_ID, self.TEST_CLIENT_SECRET)

    @pytest.mark.unit
    @responses.activate
    @pytest.mark.parametrize(
        "status_code", [400, 401, 403, 404, 405, 409, 422, 500, 501, 502, 503, 504]
    )
    def test_request_http_error(self, status_code):
        # Arrange
        responses.add(
            responses.GET,
            "https://api.tidio.com/test",
            json={"error": "HTTP Error"},
            status=status_code,
        )

        # Act & Assert
        with pytest.raises(TidioApiError, match="Tidio API request failed"):
            self.sut.get("/test")

    @pytest.mark.unit
    @responses.activate
    def test_request_connection_error(self):
        # Arrange
        responses.add(
            responses.GET,
            "https://api.tidio.com/test",
            body=responses.ConnectionError("Connection error"),
        )

        # Act & Assert
        with pytest.raises(TidioApiError, match="Tidio API request failed"):
            self.sut.get("/test")

    @pytest.mark.unit
    @responses.activate
    def test_request_timeout(self):
        # Arrange
        responses.add(
            responses.GET,
            "https://api.tidio.com/test",
            body=requests.exceptions.Timeout("Request timed out"),
        )

        # Act & Assert
        with pytest.raises(TidioApiError, match="Tidio API request timed out."):
            self.sut.get("/test")

    @pytest.mark.unit
    @responses.activate
    @pytest.mark.parametrize("body_content", [None, "", "{}"])
    def test_request_empty_response(self, body_content):
        # Arrange
        responses.add(
            responses.PUT,
            "https://api.tidio.com/test",
            body=body_content,
            status=202,
        )

        # Act
        result = self.sut.put("/test")

        # Assert
        assert result == {}

    @pytest.mark.unit
    @responses.activate
    def test_request_verifies_headers(self):
        # Arrange
        responses.add(
            responses.GET,
            "https://api.tidio.com/test",
            json={},
            status=200,
        )

        # Act
        self.sut.get("/test")

        # Assert
        request = responses.calls[0].request
        assert request.headers["X-Tidio-Openapi-Client-Id"] == self.TEST_CLIENT_ID
        assert (
            request.headers["X-Tidio-Openapi-Client-Secret"] == self.TEST_CLIENT_SECRET
        )
        assert request.headers["Accept"] == self.ACCEPT_HEADER

    @pytest.mark.unit
    @responses.activate
    def test_get_method(self):
        # Arrange
        response_data = {"data": [{"id": "1530ab70-5cad-40ed-bfcc-0c19be5e7977"}]}

        responses.add(
            responses.GET,
            "https://api.tidio.com/test",
            json=response_data,
            status=200,
        )

        # Act
        result = self.sut.get("/test")

        # Assert
        assert result == response_data
        assert len(responses.calls) == 1

    @pytest.mark.unit
    @responses.activate
    def test_post_method(self):
        # Arrange
        request_data = {"name": "John Doe"}
        response_data = {"id": "c3582dae-2f86-4e3c-9003-ef80d522578c"}

        responses.add(
            responses.POST,
            "https://api.tidio.com/test",
            json=response_data,
            status=201,
        )

        # Act
        result = self.sut.post("/test", json_data=request_data)

        # Assert
        assert result == response_data
        assert len(responses.calls) == 1

        request = responses.calls[0].request
        assert json.loads(request.body) == request_data

    @pytest.mark.unit
    @responses.activate
    def test_patch_method(self):
        # Arrange
        request_data = {"priority": "urgent"}

        responses.add(
            responses.PATCH,
            "https://api.tidio.com/test",
            status=204,
        )

        # Act
        result = self.sut.patch("/test", json_data=request_data)

        # Assert
        assert result == {}
        assert len(responses.calls) == 1

        request = responses.calls[0].request
        assert json.loads(request.body) == request_data

    @pytest.mark.unit
    @responses.activate
    def test_delete_method(self):
        # Arrange
        responses.add(
            responses.DELETE,
            "https://api.tidio.com/test",
            status=204,
        )

        # Act
        result = self.sut.delete("/test")

        # Assert
        assert result == {}
        assert len(responses.calls) == 1

    @pytest.mark.unit
    @responses.activate
    def test_put_method(self):
        # Arrange
        request_data = {"name": "John Doe"}

        responses.add(
            responses.PUT,
            "https://api.tidio.com/test",
            status=204,
        )

        # Act
        result = self.sut.put("/test", json_data=request_data)

        # Assert
        assert result == {}
        assert len(responses.calls) == 1

        request = responses.calls[0].request
        assert json.loads(request.body) == request_data
