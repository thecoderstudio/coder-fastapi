from coderfastapi.lib.security.policies.authentication.jwt import RecoveryDataProvider


def test_recovery_data_provider_augment_request(mocker):
    request_mock = mocker.MagicMock()
    provider = RecoveryDataProvider()
    request = provider.augment_request(request_mock, {"recovery": True})
    assert request.recovery
    assert request is not request_mock


def test_recovery_data_provider_augment_request_not_in_recovery(mocker):
    request_mock = mocker.MagicMock()
    provider = RecoveryDataProvider()
    request = provider.augment_request(request_mock, {})
    assert not request.recovery


def test_recovery_data_provider_parse_to_encode():
    provider = RecoveryDataProvider()
    data = provider.parse_to_encode({"recovery": True})
    assert data == {"recovery": True}


def test_recovery_data_provider_parse_to_encode_default():
    provider = RecoveryDataProvider()
    data = provider.parse_to_encode({})
    assert data == {"recovery": False}
