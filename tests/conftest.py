import uuid
from datetime import timedelta
from secrets import token_hex
from unittest.mock import MagicMock

from pytest import fixture

from coderfastapi.lib.security.policies.authentication.user import (
    UserAuthenticationPolicy,
)
from tests import create_request_with_session_mock


@fixture
def request_with_session_mock() -> MagicMock:
    return create_request_with_session_mock()


@fixture
def jwt_secret() -> str:
    return token_hex(32)


@fixture
def access_token(jwt_secret: str) -> str:
    policy = UserAuthenticationPolicy(jwt_secret)
    return policy.create_access_token(uuid.uuid4(), timedelta(minutes=10))
