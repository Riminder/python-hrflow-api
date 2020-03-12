"""A wrapper for base64 (python2 compatibility)."""
import sys
import base64


def _decodebytes_py3(input):
    return base64.decodebytes(input)


def _decodebytes_py2(input):
    return base64.b64decode(input)


def decodebytes(input):
    """Decode base64 string to byte array."""
    py_version = sys.version_info[0]
    if py_version >= 3:
        return _decodebytes_py3(input)
    return _decodebytes_py2(input)
