from fastapi import APIRouter, FastAPI

from coderfastapi.lib.validation.schemas import VersionSchema


def register_version_handler(
    router: APIRouter | FastAPI,
    version: str,
    path: str = "/",
) -> None:
    """Register a GET endpoint that returns the API version."""

    @router.get(path, response_model=VersionSchema)
    async def get_version():
        return {"version": version}
