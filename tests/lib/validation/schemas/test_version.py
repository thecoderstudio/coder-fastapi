from coderfastapi.lib.validation.schemas import VersionSchema


def test_version_schema():
    version = '1.0.1'
    schema = VersionSchema(version=version)
    assert schema.version == version
