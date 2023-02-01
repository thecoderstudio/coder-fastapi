import inspect

from fastapi import APIRouter, Request

from coderfastapi.lib.security.policies.authentication import AuthenticationPolicy
from coderfastapi.lib.security.policies.authorization import AuthorizationPolicy
from coderfastapi.lib.signature import copy_parameters


class SecureRouter(APIRouter):
    authentication_policy: AuthenticationPolicy
    authorization_policy: AuthorizationPolicy

    def __init__(
        self,
        authentication_policy: AuthenticationPolicy,
        authorization_policy: AuthorizationPolicy,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.authentication_policy = authentication_policy
        self.authorization_policy = authorization_policy

    async def _call_handler_with_authentication(
        self,
        handler,
        permission: str,
        request: Request,
        *args,
        **kwargs,
    ):
        authenticated_request = self.authentication_policy.authenticate_request(request)
        self.authorization_policy.validate_permission(permission, authenticated_request)

        output = handler(*args, **kwargs)
        if inspect.iscoroutine(output):
            output = await output

        return output

    def post(self, *outer_args, **outer_kwargs):
        return lambda func: self._http_method(func, "post", *outer_args, **outer_kwargs)

    def put(self, *outer_args, **outer_kwargs):
        return lambda func: self._http_method(func, "put", *outer_args, **outer_kwargs)

    def patch(self, *outer_args, **outer_kwargs):
        return lambda func: self._http_method(
            func, "patch", *outer_args, **outer_kwargs
        )

    def delete(self, *outer_args, **outer_kwargs):
        return lambda func: self._http_method(
            func, "delete", *outer_args, **outer_kwargs
        )

    def get(self, *outer_args, **outer_kwargs):
        return lambda func: self._http_method(func, "get", *outer_args, **outer_kwargs)

    def options(self, *outer_args, **outer_kwargs):
        return lambda func: self._http_method(
            func, "options", *outer_args, **outer_kwargs
        )

    def trace(self, *outer_args, **outer_kwargs):
        return lambda func: self._http_method(
            func, "trace", *outer_args, **outer_kwargs
        )

    def head(self, *outer_args, **outer_kwargs):
        return lambda func: self._http_method(func, "head", *outer_args, **outer_kwargs)

    def _http_method(
        self,
        func,
        http_method: str,
        *outer_args,
        permission: str = "public",
        **outer_kwargs,
    ):
        route = getattr(super(SecureRouter, self), http_method)

        @route(*outer_args, **outer_kwargs)
        async def wrapped(request: Request, *args, **kwargs):
            return await self._call_handler_with_authentication(
                func, permission, request, *args, **kwargs
            )

        wrapped_signature = inspect.signature(wrapped)
        func_signature = inspect.signature(func)
        wrapped.__signature__ = copy_parameters(
            wrapped_signature, func_signature, ["request"]
        )
        return wrapped
