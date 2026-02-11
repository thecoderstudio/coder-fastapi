import logging
from typing import Any
from uuid import UUID

from coderfastapi.lib.security.policies.authentication.jwt.providers import (
    JWTDataProvider,
    T,
)

log = logging.getLogger(__name__)


class UserDataProvider(JWTDataProvider):
    """JWT provider that extracts and encodes user identity from tokens."""

    def augment_request(self, request: T, data: dict[str, Any]) -> T:
        request_ = super().augment_request(request, data)
        try:
            user_id = UUID(data["user_id"])
            request_.user_id = user_id  # ty: ignore[unresolved-attribute]
            log.info(f"Authenticated user: {user_id}")
        except (KeyError, ValueError):
            request_.user_id = None  # ty: ignore[unresolved-attribute]

        return request_

    def parse_to_encode(self, data: dict[str, Any]) -> dict[str, Any]:
        return {"user_id": str(data["user_id"])}
