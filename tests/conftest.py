import uuid
from datetime import timedelta
from secrets import token_hex
from unittest.mock import MagicMock

from pytest import fixture

from coderfastapi.lib.security.policies.authentication.jwt import (
    JWTAuthenticationPolicy,
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
    policy = JWTAuthenticationPolicy(jwt_secret)
    return policy.create_access_token(user_id=uuid.uuid4(), delta=timedelta(minutes=10))
