from pytest import fixture

from tests.lib.security import get_acl_provider_mock


@fixture
def mock_context_acl_provider(mocker):
    def generate_context_acl_provider(acl=[]):
        return get_acl_provider_mock(mocker, acl)

    return generate_context_acl_provider
