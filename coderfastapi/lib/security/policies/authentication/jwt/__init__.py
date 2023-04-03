import copy
import logging
from collections import OrderedDict
from typing import Any, TypeVar

from fastapi import Request
from jose import JWTError, jwt

from coderfastapi.lib.security.policies.authentication import AuthenticationPolicy
from coderfastapi.lib.security.policies.authentication.jwt.providers import (
    JWTDataProvider,
)
from coderfastapi.lib.security.policies.authentication.jwt.providers.expiration import (
    ExpirationDataProvider,
)
from coderfastapi.lib.security.policies.authentication.jwt.providers.recovery import (
    RecoveryDataProvider,
)
from coderfastapi.lib.security.policies.authentication.jwt.providers.user import (
    UserDataProvider,
)

log = logging.getLogger(__name__)
T = TypeVar("T", bound=Request)
DEFAULT_PROVIDERS: set[JWTDataProvider] = {
    ExpirationDataProvider(),
    RecoveryDataProvider(),
    UserDataProvider(),
}


class JWTAuthenticationPolicy(AuthenticationPolicy):
    secret_key: str
    algorithm: str
    providers: set[JWTDataProvider]

    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        providers: set[JWTDataProvider] = DEFAULT_PROVIDERS,
    ) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.providers = providers

    def authenticate_request(self, request: T) -> T:
        request_ = copy.copy(request)
        auth_method, token = self._get_auth_method_and_token(request_.headers)
        if auth_method != "Bearer":
            token = None
        request_ = self._authenticate_with_bearer(request, token)
        return request_

    @staticmethod
    def _get_auth_method_and_token(
        headers: dict[str, Any]
    ) -> tuple[str, str] | tuple[None, None]:
        try:
            return get_auth_method_and_token(headers["authorization"])
        except KeyError:
            return (None, None)

    def _authenticate_with_bearer(self, request: T, access_token: str | None) -> T:
        request_ = request
        decoded_data = self._decode_access_token(access_token) if access_token else {}
        for provider in self.providers:
            request_ = provider.augment_request(request_, decoded_data)
        return request_

    def _decode_access_token(self, access_token: str) -> dict[str, Any]:
        try:
            return jwt.decode(
                access_token,
                self.secret_key,
                algorithms=[self.algorithm],
            )
        except (JWTError, KeyError, ValueError):
            return {}

    def create_access_token(self, **kwargs) -> str:
        data = {}
        for provider in self.providers:
            try:
                data.update(provider.parse_to_encode(kwargs))
            except KeyError:
                pass
        return self._create_token(OrderedDict(sorted(data.items())))

    def _create_token(self, data: dict[str, Any]) -> str:
        return jwt.encode(data, self.secret_key, algorithm=self.algorithm)


def get_auth_method_and_token(
    authorization_header: str,
) -> tuple[str, str] | tuple[None, None]:
    try:
        auth_method, token_string = authorization_header.split(" ")
        return auth_method, token_string
    except (AttributeError, ValueError):
        return None, None
