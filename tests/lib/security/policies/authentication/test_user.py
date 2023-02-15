import uuid
from datetime import datetime, timedelta

import pytest
from jose import jwt

from coderfastapi.lib.security.policies.authentication.user import (
    UserAuthenticationPolicy,
)

FAKE_KEY = "a877c2fd025963e0ac75aa867e290b7be3815ba9fd88d567fa6e0529721f33c9"
FAKE_TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZjUwZjAzMzMtZDc5MS"
    "00NzIzLWI3ZjktMmY2YmMyNDY0NTIxIiwiZXhwIjoxNjc1MTgwMjE2fQ.2CFaK9d_QGdVw8"
    "YIFjOnPYOPEbcvRKZjCLtG4WPyKYg"
)
TOKEN_WITHOUT_USER_ID = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzUx"
    "ODAyMTZ9.nqNzOqZvr8w4nWQL90uN_5ExWnYiNbGW2aPMzoq0-kc"
)
TOKEN_WITH_MALFORMED_USER_ID = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZjUwZjAzMzMtZDc5MS"
    "00NzIzLWI3ZjktMmY2YmMyNDY0NTIiLCJleHAiOjE2NzUxODAyMTZ9.H2ZKCdlMnEn_-gh0"
    "04E4otEacqdASPunuywiAsQJiek"
)


@pytest.mark.parametrize("recovery", [True, False])
def test_authenticate_request_success(request_with_session_mock, recovery):
    user_id = uuid.uuid4()
    policy = UserAuthenticationPolicy(FAKE_KEY)
    access_token = policy.create_access_token(user_id, timedelta(minutes=1), recovery)
    request_with_session_mock.user_id = None
    request_with_session_mock.headers = {"authorization": f"Bearer {access_token}"}

    authenticated_connection = policy.authenticate_request(request_with_session_mock)
    assert authenticated_connection.user_id == user_id
    assert authenticated_connection.recovery is recovery
    assert request_with_session_mock.user_id is None


@pytest.mark.parametrize(
    "headers",
    [
        {},
        {"authorization": "fake"},
        {"authorization": f"wrongmethod {FAKE_TOKEN}"},
        {"authorization": "Bearer fake"},
        {"authorization": f"Bearer {TOKEN_WITHOUT_USER_ID}"},
        {"authorization": f"Bearer {TOKEN_WITH_MALFORMED_USER_ID}"},
    ],
)
def test_authenticate_request_failure(request_with_session_mock, headers):
    policy = UserAuthenticationPolicy(FAKE_KEY)
    request_with_session_mock.headers = headers

    unauthenticated_connection = policy.authenticate_request(request_with_session_mock)

    assert unauthenticated_connection.user_id is None


@pytest.mark.parametrize(
    "recovery, user_id", ([(True, uuid.uuid4()), (False, None), (False, uuid.uuid4())])
)
def test_create_access_token(mocker, recovery, user_id):
    policy = UserAuthenticationPolicy(FAKE_KEY)
    now = datetime.utcnow()
    datetime_mock = mocker.patch(
        "coderfastapi.lib.security.policies.authentication.user.datetime"
    )
    datetime_mock.utcnow.return_value = now
    delta = timedelta(minutes=1)
    expected_exp = now + delta

    token = policy.create_access_token(user_id, delta, recovery)

    decoded = jwt.decode(token, FAKE_KEY, algorithms=[policy.algorithm])
    assert decoded == {
        "user_id": str(user_id),
        "exp": int(expected_exp.timestamp()),
        "recovery": recovery,
    }
