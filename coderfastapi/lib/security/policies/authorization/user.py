import logging

from fastapi.requests import HTTPConnection

from coderfastapi.lib.security import Authenticated
from coderfastapi.lib.security.policies.authorization import AuthorizationPolicy

log = logging.getLogger(__name__)


class UserAuthorizationPolicy(AuthorizationPolicy):
    @classmethod
    def get_principals(cls, http_connection: HTTPConnection):
        principals = super().get_principals(http_connection)

        authenticated_user_id = http_connection.user_id
        if authenticated_user_id:
            principals = cls._with_authenticated_user_principals(
                authenticated_user_id,
                principals,
            )

        log.debug(f"Found principals: {principals}")

        return principals

    @staticmethod
    def _with_authenticated_user_principals(
        principals: tuple[str, ...],
        authenticated_user_id: str,
    ) -> tuple[str, ...]:
        return principals + (Authenticated, f"user:{authenticated_user_id}")
