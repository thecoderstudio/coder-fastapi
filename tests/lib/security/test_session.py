import uuid
from datetime import timedelta

import pytest

from coderfastapi.lib.security.session.user import SESSION_KEY_FORMAT


async def test_create_new_session(user_session_manager):
    expected_ttl = user_session_manager.session_ttl
    user_id = uuid.uuid4()

    session = await user_session_manager.create_session(user_id)

    assert session.user_id == user_id
    persisted_session = await user_session_manager.get_session_by_id(session.id)
    assert session.id == persisted_session.id
    assert persisted_session.user_id == user_id
    assert persisted_session.remaining_ttl.total_seconds() == pytest.approx(
        expected_ttl.total_seconds()
    )


async def test_additional_session(user_session_manager):
    user_id = uuid.uuid4()
    session = await user_session_manager.create_session(user_id)
    additional_session = await user_session_manager.create_session(user_id)

    assert await user_session_manager.get_session_by_id(session.id) == session
    assert (
        await user_session_manager.get_session_by_id(additional_session.id)
        == additional_session
    )
    assert session.id != additional_session.id


async def test_get_session_by_id(user_session_manager, redis_connection):
    expected_ttl = timedelta(minutes=10)
    user_id = uuid.uuid4()
    session_id = "sessionid"
    await redis_connection.set(
        SESSION_KEY_FORMAT.format(session_id=session_id),
        str(user_id),
        ex=int(expected_ttl.total_seconds()),
    )

    session = await user_session_manager.get_session_by_id(session_id)

    assert session.id == session_id
    assert session.user_id == user_id
    assert session.remaining_ttl.total_seconds() == pytest.approx(
        expected_ttl.total_seconds()
    )


async def test_get_session_by_id_for_non_existent_session(user_session_manager):
    session = await user_session_manager.get_session_by_id("nonexistent")
    assert session is None


async def test_get_session_by_id_for_non_expiring_session(
    user_session_manager,
    redis_connection,
):
    session_id = "sessionid"
    user_id = uuid.uuid4()
    await redis_connection.set(
        SESSION_KEY_FORMAT.format(session_id=session_id),
        str(user_id),
    )

    session = await user_session_manager.get_session_by_id(session_id)

    assert session is None


async def test_expire_session(user_session_manager):
    user_id = uuid.uuid4()
    session = await user_session_manager.create_session(user_id)
    await user_session_manager.expire_session(session.id)
    exists = await user_session_manager.get_session_by_id(session.id) is not None
    assert not exists


async def test_expire_non_existent_session(user_session_manager):
    user_id = uuid.uuid4()
    session = await user_session_manager.create_session(user_id)
    await user_session_manager.expire_session("nonexistent")
    exists = await user_session_manager.get_session_by_id(session.id) is not None
    assert exists
