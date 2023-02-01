from pytest_mock import MockerFixture

from coderfastapi.lib.security.acl import ACL
from coderfastapi.lib.security.policies.authorization import AuthorizationPolicy
from tests.lib.security import get_acl_provider_mock


def get_authorization_policy_with_mock(
    mocker: MockerFixture,
    acl: ACL = (),
) -> AuthorizationPolicy:
    return AuthorizationPolicy(get_acl_provider_mock(mocker, acl))
