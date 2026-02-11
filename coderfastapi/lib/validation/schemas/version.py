from pydantic import BaseModel


class VersionSchema(BaseModel):
    """Schema containing raw version string."""

    version: str
