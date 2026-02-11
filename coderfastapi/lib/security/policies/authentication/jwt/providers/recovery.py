import logging
from typing import Any

from coderfastapi.lib.security.policies.authentication.jwt.providers import (
    JWTDataProvider,
    T,
)

log = logging.getLogger(__name__)


class RecoveryDataProvider(JWTDataProvider):
    """JWT provider that handles the recovery mode flag on requests and tokens."""

    def augment_request(self, request: T, data: dict[str, Any]) -> T:
        request_ = super().augment_request(request, data)
        recovery = data.get("recovery", False)
        request_.recovery = recovery  # ty: ignore[unresolved-attribute]
        log.info(f"Recovery mode: {recovery}")
        return request_

    def parse_to_encode(self, data: dict[str, Any]) -> dict[str, Any]:
        return {"recovery": data["recovery"]}
