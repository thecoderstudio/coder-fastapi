from contextlib import contextmanager
from http import HTTPStatus

import pytest
from fastapi.exceptions import HTTPException


@contextmanager
def raises_http_forbidden():
    with pytest.raises(HTTPException) as e:
        yield e
    exc = e.value
    assert exc.status_code == HTTPStatus.FORBIDDEN
    assert exc.detail == "Permission denied."
