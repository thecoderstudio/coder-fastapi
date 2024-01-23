from dataclasses import dataclass
from uuid import UUID

from coderfastapi.lib.security.session.base import Session, SessionManager

SECONDS_IN_MINUTE = 60
SESSION_KEY_FORMAT = "user_session:{session_id}"


@dataclass
class UserSession(Session):
    user_id: UUID


class UserSessionManager(SessionManager):
    async def create_session(self, user_id: UUID) -> UserSession:
        session = await self._create_session(str(user_id))
        return UserSession(
            id=session.id,
            user_id=user_id,
            remaining_ttl=session.remaining_ttl,
        )

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

    @staticmethod
    def _session_key(session_id: str) -> str:
        return SESSION_KEY_FORMAT.format(session_id=session_id)
