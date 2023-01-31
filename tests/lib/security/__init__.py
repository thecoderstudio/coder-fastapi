from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from coderfastapi.lib.security.acl import ACL


def get_acl_provider_mock(mocker: MockerFixture, acl: ACL) -> MagicMock:
    return mocker.MagicMock(__acl__=mocker.MagicMock(return_value=acl))
