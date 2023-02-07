import pytest
from fastapi import Depends

from coderfastapi.lib.router import SecureRouter
from coderfastapi.lib.security import Allow, Authenticated
from coderfastapi.lib.security.acl import ACLProvider
from coderfastapi.lib.security.policies.authentication.user import (
    UserAuthenticationPolicy,
)
from coderfastapi.lib.security.policies.authorization.user import (
    UserAuthorizationPolicy,
)
from tests import create_request_with_session_mock
from tests.asserts import raises_http_forbidden

# permission, authenticated, expected result
permission_expectations = [
    ("public", False, True),
    ("public", True, True),
    ("authenticated", False, False),
    ("authenticated", True, True),
    ("no_access", True, False),
]

testable_http_methods = [
    "post",
    "put",
    "patch",
    "delete",
    "get",
    "options",
    "trace",
    "head",
]


class ContextACLProvider(ACLProvider):
    def __init__(self):
        super().__init__(((Allow, Authenticated, "context_access"),))


@pytest.mark.parametrize("permission,authenticated,permitted", permission_expectations)
@pytest.mark.parametrize("http_method", testable_http_methods)
async def test_secure_router_http_methods_permissions(
    jwt_secret,
    access_token,
    permission,
    authenticated,
    permitted,
    http_method,
):
    router_acl, request_mock = generate_http_test_parameters(
        authenticated, access_token
    )

    if permitted:
        await call_http_method_decorated_mock(
            http_method, router_acl, permission, request_mock, jwt_secret
        )
    else:
        with raises_http_forbidden():
            await call_http_method_decorated_mock(
                http_method, router_acl, permission, request_mock, jwt_secret
            )


def generate_http_test_parameters(authenticated, access_token):
    headers = {}
    if authenticated:
        headers["authorization"] = f"Bearer {access_token}"
    router_acl = (
        (Allow, Authenticated, "authenticated"),
        (Allow, "nobody", "no_access"),
    )
    request_mock = create_request_with_session_mock(headers=headers)

    return router_acl, request_mock


async def call_http_method_decorated_mock(
    http_method, router_acl, permission, request_mock, jwt_secret
):
    acl_provider = ACLProvider(router_acl)
    router = SecureRouter(
        UserAuthenticationPolicy(jwt_secret),
        UserAuthorizationPolicy(acl_provider),
    )
    route_decorator = getattr(router, http_method)

    @route_decorator("/test", permission=permission)
    def endpoint_mock():
        pass

    @route_decorator("/test_async", permission=permission)
    async def async_endpoint_mock():
        pass

    await endpoint_mock(request=request_mock)
    await async_endpoint_mock(request=request_mock)


async def test_secure_router_context_acl_provider_permissions(jwt_secret, access_token):
    router_acl, request_mock = generate_http_test_parameters(True, access_token)

    acl_provider = ACLProvider(router_acl)
    router = SecureRouter(
        UserAuthenticationPolicy(jwt_secret),
        UserAuthorizationPolicy(acl_provider),
    )

    expected_context = ContextACLProvider()

    async def get_context():
        return expected_context

    @router.post("/test_async", permission="context_access")
    async def async_endpoint_mock(context=Depends(get_context)):
        assert context is expected_context

    await async_endpoint_mock(request=request_mock, context=await get_context())
