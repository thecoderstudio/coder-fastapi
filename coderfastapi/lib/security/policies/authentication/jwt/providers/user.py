import logging
from typing import Any
from uuid import UUID

from coderfastapi.lib.security.policies.authentication.jwt.providers import (
    JWTDataProvider,
    T,
)

log = logging.getLogger(__name__)


class UserDataProvider(JWTDataProvider):
    def augment_request(self, request: T, data: dict[str, Any]) -> T:
        request_ = super().augment_request(request, data)
        try:
            request_.user_id = UUID(data["user_id"])
            log.info(f"Authenticated user: {request_.user_id}")
        except (KeyError, ValueError):
            request_.user_id = None

        return request_

    def parse_to_encode(self, data: dict[str, Any]) -> dict[str, Any]:
        return {"user_id": str(data["user_id"])}
