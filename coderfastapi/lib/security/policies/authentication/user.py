import copy
import logging
from datetime import datetime, timedelta
from typing import Optional, TypeVar
from uuid import UUID

from jose import JWTError, jwt

from coderfastapi.lib.requests import RequestWithSession
from coderfastapi.lib.security.policies.authentication import AuthenticationPolicy

log = logging.getLogger(__name__)
T = TypeVar("T", bound=RequestWithSession)


class UserAuthenticationPolicy(AuthenticationPolicy):
    secret_key: str
    algorithm: str

    def __init__(self, secret_key: str, algorithm: str = "HS256") -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm

    def authenticate_request(self, request: T) -> T:
        return self._set_current_user_id(request)

    def _set_current_user_id(self, request: T) -> T:
        request_ = copy.copy(request)
        request_.user_id = self._get_authenticated_user_id(request_.headers)
        return request_

    def _get_authenticated_user_id(self, headers: dict) -> Optional[UUID]:
        try:
            auth_method, access_token = get_auth_method_and_token(
                headers["authorization"]
            )
            if auth_method != "Bearer":
                return None

            decoded = jwt.decode(
                access_token,
                self.secret_key,
                algorithms=[self.algorithm],
            )
            user_id = UUID(decoded["user_id"])
        except (JWTError, KeyError, ValueError):
            return None

        log.info(f"Authenticated user: {user_id}")
        return user_id

    def create_access_token(self, user_id: UUID, delta: timedelta) -> str:
        return jwt.encode(
            {"user_id": str(user_id), "exp": datetime.utcnow() + delta},
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
