from dataclasses import dataclass
from datetime import timedelta
from secrets import token_urlsafe
from uuid import UUID

from codercore.lib.redis import Redis

SECONDS_IN_MINUTE = 60
SESSION_ID_BYTE_LENGTH = 32
SESSION_KEY_FORMAT = "user_session:{session_id}"


@dataclass
class UserSession:
    id: str
    user_id: UUID
    remaining_ttl: timedelta


class UserSessionManager:
    cache_connection: Redis
    session_ttl: int

    def __init__(self, cache_connection: Redis, session_ttl: timedelta) -> None:
        self.cache_connection = cache_connection
        self.session_ttl = session_ttl

    async def create_session(self, user_id: UUID) -> UserSession:
        session_id = self._generate_session_id()
        ttl = self.session_ttl
        await self.cache_connection.set(
            self._session_key(session_id),
            str(user_id),
            ex=int(self.session_ttl.total_seconds()),
        )
        return UserSession(id=session_id, user_id=user_id, remaining_ttl=ttl)

    async def get_session_by_id(self, session_id: str) -> UserSession | None:
        if (user_id := await self._get_user_id_for_session(session_id)) and (
            ttl := await self._get_remaining_ttl_for_session(session_id)
        ):
            return UserSession(id=session_id, user_id=user_id, remaining_ttl=ttl)

    async def _get_user_id_for_session(self, session_id: str) -> UUID | None:
        if user_id_bytes := await self.cache_connection.get(
            self._session_key(session_id)
        ):
            return UUID(user_id_bytes.decode())

    async def _get_remaining_ttl_for_session(self, session_id: str) -> timedelta | None:
        ttl_in_seconds = await self.cache_connection.ttl(self._session_key(session_id))
        if ttl_in_seconds < 0:
            return None
        return timedelta(seconds=ttl_in_seconds)

    async def expire_session(self, session_id: str) -> None:
        await self.cache_connection.delete(self._session_key(session_id))

    @staticmethod
    def _session_key(session_id: str) -> str:
        return SESSION_KEY_FORMAT.format(session_id=session_id)

    @staticmethod
    def _generate_session_id() -> str:
        return token_urlsafe(SESSION_ID_BYTE_LENGTH)
