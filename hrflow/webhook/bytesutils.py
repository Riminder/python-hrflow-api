"""Some function to manipulate bytes(py2 compatibility)."""

import sys


def _strtobytes_py2(input, encoding):
    return bytearray(input, encoding)


def _strtobytes_py3(input, encoding):
    return bytes(input, encoding)


def strtobytes(input, encoding):
    """Take a str and transform it into a byte array."""
    py_version = sys.version_info[0]
    if py_version >= 3:
        return _strtobytes_py3(input, encoding)
    return _strtobytes_py2(input, encoding)
