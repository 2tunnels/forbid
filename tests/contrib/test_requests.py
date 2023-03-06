from unittest.mock import Mock, patch

import pytest
import requests

from forbid.contrib.requests import forbid_requests
from forbid.exceptions import ForbiddenError


@patch("requests.sessions.Session.send", autospec=True)
def test_requests(mocked_send: Mock):
    requests.get("https://example.com")
    mocked_send.assert_called_once()
    mocked_send.reset_mock()

    with forbid_requests(), pytest.raises(ForbiddenError) as exc_info:
        requests.get("https://example.com")

    assert repr(exc_info.value) == "ForbiddenError('requests.sessions.Session.request was called')"

    mocked_send.assert_not_called()
    mocked_send.reset_mock()

    requests.get("https://example.com")
    mocked_send.assert_called_once()
    mocked_send.reset_mock()
