from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import timedelta
from secrets import token_urlsafe
from typing import TypeVar

from codercore.lib.redis import Redis

SESSION_ID_BYTE_LENGTH = 32


@dataclass
class Session:
    id: str
    remaining_ttl: timedelta


T = TypeVar("T", bound=Session)


class SessionManager(metaclass=ABCMeta):
    cache_connection: Redis
    session_ttl: int

    def __init__(self, cache_connection: Redis, session_ttl: timedelta) -> None:
        self.cache_connection = cache_connection
        self.session_ttl = session_ttl

    @abstractmethod
    async def create_session(self, value: str) -> T:
        """Stores new session in cache, returns created session object."""

    async def _create_session(self, value: str) -> Session:
        session_id = self._generate_session_id()
        ttl = self.session_ttl
        await self.cache_connection.set(
            self._session_key(session_id),
            value,
            ex=int(self.session_ttl.total_seconds()),
        )
        return Session(id=session_id, remaining_ttl=ttl)

    @abstractmethod
    async def get_session_by_id(self, session_id: str) -> T:
        """Gets the session for the given session_id, if it exists in the cache."""

    async def _get_remaining_ttl_for_session(self, session_id: str) -> timedelta | None:
        ttl_in_seconds = await self.cache_connection.ttl(self._session_key(session_id))
        if ttl_in_seconds < 0:
            return None
        return timedelta(seconds=ttl_in_seconds)

    async def expire_session(self, session_id: str) -> None:
        await self.cache_connection.delete(self._session_key(session_id))

    @staticmethod
    @abstractmethod
    def _session_key(session_id: str) -> str:
        """Returns a formatted session key for the given session_id."""

    @staticmethod
    def _generate_session_id() -> str:
        return token_urlsafe(SESSION_ID_BYTE_LENGTH)
