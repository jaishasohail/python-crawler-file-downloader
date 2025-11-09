import sys
pathlib import Path

# Ensure src is on path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import logging  # noqa: E402
from crawler.authenticator import create_session  # noqa: E402


def test_create_session_applies_headers_and_cookies():
    logger = logging.getLogger("test_auth")
    auth_config = {
        "headers": {"X-Test-Header": "value"},
        "cookies": {"sessionid": "abc123"},
        # No login_url so we don't perform network I/O in the test
        "login_url": None,
    }

    session = create_session(auth_config, logger)

    assert session.headers.get("X-Test-Header") == "value"
    assert session.cookies.get("sessionid") == "abc123"
