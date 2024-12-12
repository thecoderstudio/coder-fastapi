import uuid

from coderfastapi.lib.security import Authenticated, Everyone
from coderfastapi.lib.security.policies.authorization.user import (
    RecoverableUserAuthorizationPolicy,
    UserAuthorizationPolicy,
)
from tests.lib.security import get_acl_provider_mock


async def test_user_auth_policy_unauthenticated(mocker, request_with_session_mock):
    policy = UserAuthorizationPolicy(get_acl_provider_mock(mocker, ()))
    request_with_session_mock.user_id = None
    principals = await policy.get_principals(request_with_session_mock)
    assert principals == (Everyone,)


async def test_user_auth_policy_authenticated(mocker, request_with_session_mock):
    user_id = uuid.uuid4()
    policy = UserAuthorizationPolicy(get_acl_provider_mock(mocker, ()))
    request_with_session_mock.user_id = user_id
    principals = await policy.get_principals(request_with_session_mock)
    assert principals == (Everyone, Authenticated, f"user:{user_id}")


async def test_recoverable_user_policy_authenticated(mocker, request_with_session_mock):
    user_id = uuid.uuid4()
    policy = RecoverableUserAuthorizationPolicy(get_acl_provider_mock(mocker, ()))
    request_with_session_mock.user_id = user_id
    request_with_session_mock.recovery = True
    principals = await policy.get_principals(request_with_session_mock)
    assert principals == (Everyone, f"recovering_user:{user_id}")


async def test_recoverable_user_policy_authenticated_not_in_recovery(
    mocker, request_with_session_mock
):
    user_id = uuid.uuid4()
    policy = RecoverableUserAuthorizationPolicy(get_acl_provider_mock(mocker, ()))
    request_with_session_mock.user_id = user_id
    request_with_session_mock.recovery = False
    principals = await policy.get_principals(request_with_session_mock)
    assert principals == (Everyone, Authenticated, f"user:{user_id}")
