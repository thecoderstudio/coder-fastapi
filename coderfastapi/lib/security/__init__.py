import logging

from fastapi import HTTPException

from coderfastapi.lib.security.acl import Allow, Authenticated, Deny, Everyone

log = logging.getLogger(__name__)


class AuthorizationPolicy:
    def __init__(self, acl_provider):
        self.acl_provider = acl_provider

    def validate_permission(
        self, requested_permission, enhanced_http_connection, context_acl_provider=None
    ):
        try:
            allowed = self.check_permission(
                requested_permission, enhanced_http_connection, context_acl_provider
            )
        except ValueError as e:
            log.exception(e)
            allowed = False

        if allowed:
            return

        raise HTTPException(status_code=403, detail="Permission denied.")

    def check_permission(
        self, requested_permission, enhanced_http_connection, context_acl_provider=None
    ):
        principals = self.get_principals(enhanced_http_connection)

        for action, principal, permission in self.get_complete_acl(
            context_acl_provider
        ):
            if permission != requested_permission or principal not in principals:
                continue

            if action is Allow:
                log.info(f"Permission '{permission}' granted")
                return True
            elif action is Deny:
                log.info(f"Permission '{permission}' denied")
                return False
            else:
                raise ValueError("Invalid action in ACL")

        return False

    @classmethod
    def get_principals(cls, enhanced_http_connection):
        principals = [Everyone]

        authenticated_user_id = enhanced_http_connection.user_id
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

    def get_complete_acl(self, context_acl_provider=None):
        acl = self.acl_provider.__acl__()
        if not context_acl_provider:
            return acl

        complete_acl = context_acl_provider.__acl__() + acl
        log.debug(f"complete ACL: {complete_acl}")

        return complete_acl
