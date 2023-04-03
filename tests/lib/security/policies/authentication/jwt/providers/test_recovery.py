import pytest

from coderfastapi.lib.security.policies.authentication.jwt import RecoveryDataProvider


@pytest.mark.parametrize("recovery", (False, True))
def test_recovery_data_provider_augment_request(mocker, recovery):
    request_mock = mocker.MagicMock()
    provider = RecoveryDataProvider()
    request = provider.augment_request(request_mock, {"recovery": recovery})
    assert request.recovery is recovery
    assert request is not request_mock


def test_recovery_data_provider_augment_request_not_in_recovery(mocker):
    request_mock = mocker.MagicMock()
    provider = RecoveryDataProvider()
    request = provider.augment_request(request_mock, {})
    assert not request.recovery


@pytest.mark.parametrize("recovery", (False, True))
def test_recovery_data_provider_parse_to_encode(recovery):
    provider = RecoveryDataProvider()
    data = provider.parse_to_encode({"recovery": recovery})
    assert data == {"recovery": recovery}
