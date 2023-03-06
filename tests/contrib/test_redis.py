from unittest.mock import Mock

import pytest
from redis import ConnectionPool, Redis

from forbid.contrib.redis import forbid_redis
from forbid.exceptions import ForbiddenError


def test_redis():
    pool = ConnectionPool()
    pool.get_connection = Mock()
    pool.get_connection.return_value.retry.call_with_retry.return_value = "bar"

    r = Redis(connection_pool=pool)

    assert r.get("foo") == "bar"
    pool.get_connection.assert_called_once()
    pool.get_connection.return_value.retry.call_with_retry.assert_called_once()
    pool.get_connection.reset_mock()

    with forbid_redis(), pytest.raises(ForbiddenError) as exc_info:
        r.set("foo", "bar")

    assert repr(exc_info.value) == "ForbiddenError('redis.client.Redis.execute_command was called')"
    pool.get_connection.assert_not_called()
    pool.get_connection.return_value.retry.call_with_retry.assert_not_called()
    pool.get_connection.reset_mock()

    assert r.get("foo") == "bar"
    pool.get_connection.assert_called_once()
    pool.get_connection.return_value.retry.call_with_retry.assert_called_once()
    pool.get_connection.reset_mock()
