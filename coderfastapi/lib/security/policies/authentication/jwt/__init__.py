import copy
import logging
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


class JWTAuthenticationPolicy(AuthenticationPolicy):
    secret_key: str
    algorithm: str
    providers: set[JWTDataProvider]

    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        providers: set[JWTDataProvider] = {
            ExpirationDataProvider(),
            RecoveryDataProvider(),
            UserDataProvider(),
        },
    ) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.providers = providers

    def authenticate_request(self, request: T) -> T:
        request_ = copy.copy(request)
        decoded_data = self._decode_access_token(request_.headers)
        for provider in self.providers:
            request_ = provider.augment_request(request_, decoded_data)
        return request_

    def _decode_access_token(self, headers: dict[str, Any]) -> dict[str, Any]:
        try:
            auth_method, access_token = get_auth_method_and_token(
                headers["authorization"]
            )
            if auth_method != "Bearer":
                return {}

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
            data.update(provider.parse_to_encode(kwargs))
        return jwt.encode(
            data,
            self.secret_key,
            algorithm=self.algorithm,
        )


def get_auth_method_and_token(
    authorization_header: str,
) -> tuple[str, str] | tuple[None, None]:
    try:
        auth_method, token_string = authorization_header.split(" ")
        return auth_method, token_string
    except (AttributeError, ValueError):
        return None, None
