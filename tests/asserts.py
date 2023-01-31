import pytest
from fastapi.exceptions import HTTPException

raises_http_forbidden = pytest.raises(HTTPException)
