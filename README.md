# Coder FastAPI

Security and utility library for building FastAPI applications with authentication, authorization, and pagination out of the box.

## Features

- **SecureRouter** — Drop-in `APIRouter` replacement that enforces authentication and ACL-based authorization on every route
- **Authentication policies** — Pluggable strategies for JWT (Bearer token) and session-based authentication
- **Authorization policies** — Pyramid-style ACL authorization with Allow/Deny rules and composable principals
- **JWT providers** — Extensible provider system for token creation and request augmentation (expiration, user data, recovery mode)
- **Session management** — Abstract session manager backed by Redis with configurable TTL and secure token generation
- **Pagination** — Cursor-based pagination decorator that auto-generates RFC 5988 `Link` headers
- **Cloud logging** — Google Cloud Logging integration with Cloud Trace context propagation middleware
- **Validation schemas** — Pydantic models for query parameters, pagination cursors, and aggregation filters

## Installation

```bash
pip install coderfastapi
```

## Quick Start

### Secure Router with JWT Authentication

```python
from coderfastapi.lib.router import SecureRouter
from coderfastapi.lib.security.acl import ACLProvider
from coderfastapi.lib.security.policies.authentication.jwt import JWTAuthenticationPolicy
from coderfastapi.lib.security.policies.authorization.user import UserAuthorizationPolicy
from fastapi import FastAPI

app = FastAPI()
authentication_policy = JWTAuthenticationPolicy(secret_key="your-secret-key")
authorization_policy = UserAuthorizationPolicy(acl_provider=ACLProvider())
router = SecureRouter(authentication_policy, authorization_policy)

@router.get("/users", permission="public")
async def list_users(request):
    ...

app.include_router(router)
```

### Session Management

```python
from datetime import timedelta

from codercore.lib.redis import connection
from coderfastapi.lib.security import UserSessionManager

cache_connection = connection(host="localhost")
session_manager = UserSessionManager(
    cache_connection=cache_connection,
    session_ttl=timedelta(hours=24),
)

session = await session_manager.create_session(user_id=str(user.id))
retrieved = await session_manager.get_session_by_id(session.id)
```

### Paginated Endpoints

```python
from coderfastapi.lib.decorators import paginate
from coderfastapi.lib.validation.schemas.query import QueryParameters

@router.get("/items")
@paginate("id")
async def list_items(params: QueryParameters = Depends()):
    ...  # return list of items. Link headers are generated automatically
```

## Requirements

- Python 3.12+
- Redis 7+ (required by session management only)

All other features — JWT authentication, authorization, pagination, cloud logging — work without Redis.

## Documentation

Build and serve the API reference locally:

```bash
pip install -e ".[docs]"
mkdocs serve
```

Then visit `http://127.0.0.1:8000`. To build static HTML:

```bash
mkdocs build
```

## Development

```bash
pip install -e ".[test,dev]"
```

### Running Tests

Tests run against a real Redis instance via Docker Compose:

```bash
docker compose -f test-compose.yml up --build
```

### Linting

This project uses [pre-commit](https://pre-commit.com/) for linting:

```bash
pre-commit install
pre-commit run --all-files
```

## License

[Apache-2.0](LICENSE)
