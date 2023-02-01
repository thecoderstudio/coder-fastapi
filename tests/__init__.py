from unittest.mock import MagicMock, patch


def create_request_with_session_mock(headers: dict = {}) -> MagicMock:
    request_mock = patch("coderfastapi.lib.requests.RequestWithSession")
    request_mock.headers = headers
    return request_mock
