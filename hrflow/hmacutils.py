"""Some utils for hash(py2 compatibility)."""

import sys
import hmac


def _compare_digest_py2(a, b):
    return a == b


def _compare_digest_py3(a, b):
    return hmac.compare_digest(a, b)


def compare_digest(a, b):
    """Compare 2 hash digest."""
    py_version = sys.version_info[0]
    if py_version >= 3:
        return _compare_digest_py3(a, b)
    return _compare_digest_py2(a, b)
