from unittest.mock import MagicMock

from pytest import fixture

from tests import create_http_connection_mock


@fixture
def http_connection_mock() -> MagicMock:
    return create_http_connection_mock()
