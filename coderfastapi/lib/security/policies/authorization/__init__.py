import logging
from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from fastapi.requests import HTTPConnection

from coderfastapi.lib.security import Allow, Deny, Everyone
from coderfastapi.lib.security.acl import ACL, ACLProvider

log = logging.getLogger(__name__)


class AuthorizationPolicy:
    acl_provider: ACLProvider

    def __init__(self, acl_provider: ACLProvider) -> None:
        self.acl_provider = acl_provider

    def validate_permission(
        self,
        requested_permission: str,
        http_connection: HTTPConnection,
        context_acl_provider: Optional[ACLProvider] = None,
    ) -> None:
        try:
            allowed = self.check_permission(
                requested_permission, http_connection, context_acl_provider
            )
        except ValueError as e:
            log.exception(e)
            allowed = False

        if allowed:
            return

        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Permission denied.",
        )

    def check_permission(
        self,
        requested_permission: str,
        http_connection: HTTPConnection,
        context_acl_provider: Optional[ACLProvider] = None,
    ) -> bool:
        principals = self.get_principals(http_connection)

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
    def get_principals(cls, http_connection: HTTPConnection) -> tuple[str, ...]:
        return (Everyone,)

    def get_complete_acl(
        self,
        context_acl_provider: Optional[ACLProvider] = None,
    ) -> ACL:
        acl = self.acl_provider.__acl__()
        if not context_acl_provider:
            return acl

        complete_acl = context_acl_provider.__acl__() + acl
        log.debug(f"complete ACL: {complete_acl}")

        return complete_acl
