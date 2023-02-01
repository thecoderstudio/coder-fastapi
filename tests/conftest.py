from unittest.mock import MagicMock

from pytest import fixture

from tests import create_request_with_session_mock


@fixture
def request_with_session_mock() -> MagicMock:
    return create_request_with_session_mock()
