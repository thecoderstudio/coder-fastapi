from datetime import datetime, timedelta

from coderfastapi.lib.security.policies.authentication.jwt import ExpirationDataProvider


def test_expiration_data_provider_augment_request(mocker):
    request_mock = mocker.MagicMock()
    provider = ExpirationDataProvider()
    request = provider.augment_request(request_mock, {})
    assert request is not request_mock


def test_expiration_data_provider_parse_to_encode(mocker):
    now = datetime.utcnow()
    datetime_mock = mocker.patch(
        "coderfastapi.lib.security.policies.authentication.jwt.providers."
        "expiration.datetime"
    )
    datetime_mock.utcnow.return_value = now
    delta = timedelta(minutes=1)
    expected_exp = now + delta

    provider = ExpirationDataProvider()
    data = provider.parse_to_encode({"delta": delta})
    assert data == {"exp": expected_exp}
