import logging

from fastapi import Request

from coderfastapi.lib.security import Authenticated
from coderfastapi.lib.security.policies.authorization import AuthorizationPolicy

log = logging.getLogger(__name__)


class UserAuthorizationPolicy(AuthorizationPolicy):
    @classmethod
    def get_principals(cls, request: Request) -> tuple[str, ...]:
        principals = super().get_principals(request)

        authenticated_user_id = request.user_id
        if authenticated_user_id:
            principals = cls._with_authenticated_user_principals(
                principals,
                str(authenticated_user_id),
            )

        log.debug(f"Found principals: {principals}")

        return principals

    @staticmethod
    def _with_authenticated_user_principals(
        principals: tuple[str, ...],
        authenticated_user_id: str,
    ) -> tuple[str, ...]:
        return principals + (Authenticated, f"user:{authenticated_user_id}")


class RecoverableUserAuthorizationPolicy(UserAuthorizationPolicy):
    @classmethod
    def get_principals(cls, request: Request) -> tuple[str, ...]:
        if not request.recovery:
            return super().get_principals(request)

        principals = AuthorizationPolicy.get_principals(request) + (
            f"recovering_user:{request.user_id}",
        )
        log.debug(f"Found principals: {principals}")
        return principals
