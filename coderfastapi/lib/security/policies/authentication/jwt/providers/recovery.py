import logging
from typing import Any

from coderfastapi.lib.security.policies.authentication.jwt.providers import (
    JWTDataProvider,
    T,
)

log = logging.getLogger(__name__)


class RecoveryDataProvider(JWTDataProvider):
    def augment_request(self, request: T, data: dict[str, Any]) -> T:
        request_ = super().augment_request(request, data)
        request_.recovery = data.get("recovery", False)
        log.info(f"Recovery mode: {request_.recovery}")
        return request_

    def parse_to_encode(self, data: dict[str, Any]) -> dict[str, Any]:
        return {"recovery": data["recovery"]}
