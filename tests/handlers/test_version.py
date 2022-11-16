from fastapi import FastAPI
from fastapi.testclient import TestClient

from coderfastapi.handlers.version import register_version_handler


def test_register_version_handler():
    app = FastAPI()
    path = "/"
    version = "1.0.1"
    register_version_handler(app, version, path)
    test_client = TestClient(app)

    response = test_client.get(path)

    assert response.status_code == 200
    assert response.json() == {"version": version}
