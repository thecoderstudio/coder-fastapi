import pytest

from coderfastapi.lib.security import Allow, Deny, Everyone
from tests.asserts import raises_http_forbidden

# (provider_acl, context_acl, permitted_expectation)
acl_permission_expectations = (
    (((Deny, Everyone, "public"),), ((Allow, Everyone, "public"),), True),
    (((Allow, Everyone, "public"),), ((Deny, Everyone, "public"),), False),
)


def test_validate_permission_allowed_with_context_provider(
    mock_policy, mock_context_acl_provider, request_with_session_mock
):
    policy = mock_policy(((Deny, Everyone, "public"),))
    policy.validate_permission(
        "public",
        request_with_session_mock,
        mock_context_acl_provider(((Allow, Everyone, "public"),)),
    )


def test_validate_permission_denied_explicit_with_context_provider(
    mock_policy, mock_context_acl_provider, request_with_session_mock
):
    policy = mock_policy(((Allow, Everyone, "public"),))
    with raises_http_forbidden():
        policy.validate_permission(
            "public",
            request_with_session_mock,
            mock_context_acl_provider(((Deny, Everyone, "public"),)),
        )


def test_validate_permission_denied_implicit(mock_policy, request_with_session_mock):
    policy = mock_policy(((Allow, Everyone, "fake"), (Allow, "test", "public")))
    with raises_http_forbidden():
        policy.validate_permission("public", request_with_session_mock)


def test_validate_permission_invalid_acl(mock_policy, request_with_session_mock):
    policy = mock_policy((("test", Everyone, "public"),))

    with raises_http_forbidden():
        policy.validate_permission("public", request_with_session_mock)


@pytest.mark.parametrize(
    "provider_acl,context_acl,expectation", acl_permission_expectations
)
def test_check_permission(
    mock_policy,
    request_with_session_mock,
    mock_context_acl_provider,
    provider_acl,
    context_acl,
    expectation,
):
    allowed = mock_policy(provider_acl).check_permission(
        "public", request_with_session_mock, mock_context_acl_provider(context_acl)
    )

    assert allowed is expectation


def test_check_permission_denied_implicit(mock_policy, request_with_session_mock):
    policy = mock_policy(((Allow, Everyone, "fake"), (Allow, "test", "public")))
    allowed = policy.check_permission("public", request_with_session_mock)

    assert allowed is False


def test_check_permission_invalid_acl(mocker, mock_policy, request_with_session_mock):
    policy = mock_policy((("fake", Everyone, "public"),))

    with pytest.raises(ValueError, match="Invalid action in ACL"):
        policy.check_permission("public", request_with_session_mock)


def test_auth_policy_minimal_principals(mock_policy, request_with_session_mock):
    principals = mock_policy().get_principals(request_with_session_mock)

    assert principals == (Everyone,)


@pytest.mark.parametrize(
    "provider_acl,context_acl,expected_acl",
    (
        (((Allow, Everyone, "public"),), (), ((Allow, Everyone, "public"),)),
        (
            ((Allow, Everyone, "public"),),
            ((Allow, "test", "fake"),),
            ((Allow, "test", "fake"), (Allow, Everyone, "public")),
        ),
    ),
)
def test_get_complete_acl(
    mock_policy,
    mock_context_acl_provider,
    provider_acl,
    context_acl,
    expected_acl,
):
    acl = mock_policy(provider_acl).get_complete_acl(
        mock_context_acl_provider(context_acl)
    )

    assert acl == expected_acl


def test_get_complete_acl_no_context_provider(mock_policy):
    policy = mock_policy(((Allow, Everyone, "public"),))

    assert policy.get_complete_acl() == ((Allow, Everyone, "public"),)
