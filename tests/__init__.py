from unittest.mock import MagicMock, patch


def create_http_connection_mock(headers: dict = {}) -> MagicMock:
    connection_mock = patch("fastapi.requests.HTTPConnection")
    connection_mock.headers = headers
    return connection_mock
