import copy
from abc import ABC, abstractmethod
from typing import Any, TypeVar

from fastapi import Request

T = TypeVar("T", bound=Request)


class JWTDataProvider(ABC):
    """Base class for JWT providers that augment requests."""

    def augment_request(self, request: T, data: dict[str, Any]) -> T:
        """Augment a request with data decoded from the JWT. Returns a shallow copy."""
        return copy.copy(request)

    @abstractmethod
    def parse_to_encode(self, data: dict[str, Any]) -> dict[str, Any]:
        """Returns data that needs to be encoded in the JWT for this provider."""
