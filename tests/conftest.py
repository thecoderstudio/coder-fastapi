import uuid
from datetime import timedelta
from secrets import token_hex
from unittest.mock import MagicMock

from codercore.lib.redis import Redis
from codercore.test.fixtures import (
    redis_connection as redis_connection_,
    redis_connection_maker as redis_connection_maker_,
)
from pytest import fixture

from coderfastapi.lib.security.policies.authentication.jwt import (
    JWTAuthenticationPolicy,
)
from coderfastapi.lib.security.session import UserSessionManager
from tests import create_request_with_session_mock

redis_connection_maker = fixture(redis_connection_maker_)
redis_connection = fixture(redis_connection_)


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


@fixture
def user_session_manager(redis_connection: Redis) -> UserSessionManager:
    return UserSessionManager(redis_connection, timedelta(minutes=10))
