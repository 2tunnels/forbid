import pytest

from forbid import forbid
from forbid.exceptions import ForbiddenError


def _uppercase(value: str) -> str:
    return value.upper()


def _shout(value: str) -> str:
    return f"{_uppercase(value)}!"


def test_forbid():
    assert _shout("hello") == "HELLO!"

    with forbid(f"{__name__}._uppercase"), pytest.raises(ForbiddenError) as exc_info:
        _shout("hello")

    assert repr(exc_info.value) == f"ForbiddenError('{__name__}._uppercase was called')"

    assert _shout("hello") == "HELLO!"
