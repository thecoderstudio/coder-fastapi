from datetime import UTC, datetime
from typing import Any

from coderfastapi.lib.security.policies.authentication.jwt.providers import (
    JWTDataProvider,
)


class ExpirationDataProvider(JWTDataProvider):
    """JWT provider that adds an expiration claim based on a timedelta."""

    def parse_to_encode(self, data: dict[str, Any]) -> dict[str, Any]:
        return {"exp": datetime.now(UTC) + data["delta"]}
