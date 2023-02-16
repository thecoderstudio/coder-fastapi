import uuid

import pytest

from coderfastapi.lib.security.policies.authentication.jwt import UserDataProvider


def test_user_data_provider_augment_request(mocker):
    user_id = uuid.uuid4()
    request_mock = mocker.MagicMock()
    provider = UserDataProvider()
    request = provider.augment_request(request_mock, data={"user_id": str(user_id)})
    assert request.user_id == user_id


@pytest.mark.parametrize("data", [{}, {"user_id": "wrong"}])
def test_user_data_provider_augment_request_no_user_id(mocker, data):
    request_mock = mocker.MagicMock()
    provider = UserDataProvider()
    request = provider.augment_request(request_mock, data)
    assert request.user_id is None


def test_user_data_provider_parse_to_encode():
    user_id = uuid.uuid4()
    provider = UserDataProvider()
    data = provider.parse_to_encode({"user_id": user_id})
    assert data == {"user_id": str(user_id)}
