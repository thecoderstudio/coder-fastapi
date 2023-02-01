import uuid

from coderfastapi.lib.security import Authenticated, Everyone
from coderfastapi.lib.security.policies.authorization.user import (
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
