import copy
from abc import ABC, abstractmethod
from typing import Any, TypeVar

from coderfastapi.lib.requests import AugmentableRequest

T = TypeVar("T", bound=AugmentableRequest)


class JWTDataProvider(ABC):
    def augment_request(self, request: T, data: dict[str, Any]) -> T:
        return copy.copy(request)

    @abstractmethod
    def parse_to_encode(self, data: dict[str, Any]) -> dict[str, Any]:
        """Returns data that needs to be encoded in the JWT for this provider."""
