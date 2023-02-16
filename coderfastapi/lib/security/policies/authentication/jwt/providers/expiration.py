from datetime import datetime
from typing import Any

from coderfastapi.lib.security.policies.authentication.jwt.providers import (
    JWTDataProvider,
)


class ExpirationDataProvider(JWTDataProvider):
    def parse_to_encode(self, data: dict[str, Any]) -> dict[str, Any]:
        return {"exp": datetime.utcnow() + data["delta"]}
