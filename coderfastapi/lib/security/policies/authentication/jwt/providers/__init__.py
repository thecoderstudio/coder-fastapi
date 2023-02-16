import copy
from abc import ABC, abstractmethod
from typing import Any, TypeVar

from fastapi import Request

T = TypeVar("T", bound=Request)


class JWTDataProvider(ABC):
    def augment_request(self, request: T, data: dict[str, Any]) -> T:
        return copy.copy(request)

    @abstractmethod
    def parse_to_encode(self, data: dict[str, Any]) -> dict[str, Any]:
        """Returns data that needs to be encoded in the JWT for this provider."""
