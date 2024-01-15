import uuid
from datetime import timedelta

from coderfastapi.lib.security.policies.authentication.session import (
    SESSION_COOKIE_KEY,
    UserSessionAuthenticationPolicy,
)
from coderfastapi.lib.security.session import UserSession


async def test_authenticate_request_success(mocker):
    session = UserSession(
        id="sessionid",
        user_id=uuid.uuid4(),
        remaining_ttl=timedelta(minutes=10),
    )
    request_mock = mocker.MagicMock()
    request_mock.cookies = {SESSION_COOKIE_KEY: session.id}
    session_manager_mock = mocker.MagicMock()
    session_manager_mock.get_session_by_id = mocker.AsyncMock(return_value=session)
    policy = UserSessionAuthenticationPolicy()

    request = await policy.authenticate_request(request_mock, session_manager_mock)

    assert request.user_id == session.user_id
    session_manager_mock.get_session_by_id.assert_awaited_once_with(session.id)


async def test_authenticate_request_no_session_id(mocker):
    request_mock = mocker.MagicMock()
    request_mock.cookies = {}
    session_manager_mock = mocker.MagicMock()
    policy = UserSessionAuthenticationPolicy()

    request = await policy.authenticate_request(request_mock, session_manager_mock)

    assert request.user_id is None


async def test_authenticate_request_invalid_session_id(mocker):
    session_id = "sessionid"
    request_mock = mocker.MagicMock()
    request_mock.cookies = {SESSION_COOKIE_KEY: session_id}
    session_manager_mock = mocker.MagicMock()
    session_manager_mock.get_session_by_id = mocker.AsyncMock(return_value=None)
    policy = UserSessionAuthenticationPolicy()

    request = await policy.authenticate_request(request_mock, session_manager_mock)

    assert request.user_id is None
    session_manager_mock.get_session_by_id.assert_awaited_once_with(session_id)
