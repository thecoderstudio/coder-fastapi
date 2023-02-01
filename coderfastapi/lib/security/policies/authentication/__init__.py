from abc import ABC, abstractmethod
from typing import TypeVar

from fastapi import Request

T = TypeVar("T", bound=Request)


class AuthenticationPolicy(ABC):
    @abstractmethod
    def authenticate_request(self, request: T) -> T:
        """Adds metadata to request if properly authenticated."""
