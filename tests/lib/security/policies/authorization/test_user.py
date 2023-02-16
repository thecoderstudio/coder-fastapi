import uuid

from coderfastapi.lib.security import Authenticated, Everyone
from coderfastapi.lib.security.policies.authorization.user import (
    RecoverableUserAuthorizationPolicy,
    UserAuthorizationPolicy,
)
from tests.lib.security import get_acl_provider_mock


def test_user_auth_policy_unauthenticated(mocker, request_with_session_mock):
    policy = UserAuthorizationPolicy(get_acl_provider_mock(mocker, ()))
    request_with_session_mock.user_id = None
    principals = policy.get_principals(request_with_session_mock)
    assert principals == (Everyone,)


def test_user_auth_policy_authenticated(mocker, request_with_session_mock):
    user_id = uuid.uuid4()
    policy = UserAuthorizationPolicy(get_acl_provider_mock(mocker, ()))
    request_with_session_mock.user_id = user_id
    principals = policy.get_principals(request_with_session_mock)
    assert principals == (Everyone, Authenticated, f"user:{user_id}")


def test_recoverable_user_policy_authenticated(mocker, request_with_session_mock):
    user_id = uuid.uuid4()
    policy = RecoverableUserAuthorizationPolicy(get_acl_provider_mock(mocker, ()))
    request_with_session_mock.user_id = user_id
    request_with_session_mock.recovery = True
    principals = policy.get_principals(request_with_session_mock)
    assert principals == (Everyone, f"recovering_user:{user_id}")


def test_recoverable_user_policy_authenticated_not_in_recovery(
    mocker, request_with_session_mock
):
    user_id = uuid.uuid4()
    policy = RecoverableUserAuthorizationPolicy(get_acl_provider_mock(mocker, ()))
    request_with_session_mock.user_id = user_id
    request_with_session_mock.recovery = False
    principals = policy.get_principals(request_with_session_mock)
    assert principals == (Everyone, Authenticated, f"user:{user_id}")
