from fastapi import APIRouter

from coderfastapi.lib.validation.schemas import VersionSchema


async def register_version_handler(
    router: APIRouter,
    version: str,
    path: str = '/'
) -> None:
    @router.get(path, response_model=VersionSchema)
    async def get_version():
        return {'version': version}
