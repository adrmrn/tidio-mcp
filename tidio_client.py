from typing import Literal

import requests


class TidioApiError(Exception):
    pass


class TidioApiClient:
    BASE_URL = "https://api.tidio.com"

    def __init__(self, client_id: str, client_secret: str):
        self.client = requests.Session()
        self.client.headers.update(
            {
                "X-Tidio-Openapi-Client-Id": client_id,
                "X-Tidio-Openapi-Client-Secret": client_secret,
                "Accept": "application/json; version=1",
            }
        )

    def get(self, endpoint: str) -> dict:
        return self._request("GET", endpoint)

    def post(self, endpoint: str, json_data: dict = None) -> dict:
        return self._request("POST", endpoint, json_data)

    def put(self, endpoint: str, json_data: dict = None) -> dict:
        return self._request("PUT", endpoint, json_data)

    def patch(self, endpoint: str, json_data: dict = None) -> dict:
        return self._request("PATCH", endpoint, json_data)

    def delete(self, endpoint: str) -> dict:
        return self._request("DELETE", endpoint)

    def _request(
        self,
        method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"],
        endpoint: str,
        json_data: dict = None,
    ) -> dict:
        """
        Raises:
            TidioApiError: For timeout or HTTP errors
        """
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.client.request(method, url, json=json_data, timeout=15)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            raise TidioApiError("Tidio API request timed out.") from None
        except requests.exceptions.RequestException as e:
            error_text = e.response.text if e.response is not None else ""
            raise TidioApiError(f"Tidio API request failed. {e} {error_text}") from None

        if not response.content:
            return {}

        return response.json()
