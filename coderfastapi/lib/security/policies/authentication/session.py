import copy
from typing import TypeVar

from fastapi import Request

from coderfastapi.lib.security import UserSessionManager
from coderfastapi.lib.security.policies.authentication import AuthenticationPolicy

SESSION_COOKIE_KEY = "session_id"
T = TypeVar("T", bound=Request)


class UserSessionAuthenticationPolicy(AuthenticationPolicy):
    @classmethod
    async def authenticate_request(
        cls,
        request: T,
        session_manager: UserSessionManager,
    ) -> T:
        request_ = copy.copy(request)
        request_.user_id = None
        session_id = cls._get_session_id_from_cookie(request.cookies)

        if not session_id:
            return request_
        if session := await session_manager.get_session_by_id(session_id):
            request_.user_id = session.user_id
        return request_

    @staticmethod
    def _get_session_id_from_cookie(cookies: dict) -> str | None:
        return cookies.get(SESSION_COOKIE_KEY)
