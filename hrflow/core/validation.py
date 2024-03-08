import os
import re

KEY_REGEX = r"^[0-9a-f]{40}$"
STAGE_VALUES = [None, "new", "yes", "later", "no"]
SORT_BY_VALUES = [
    "created_at",
    "updated_at",
    "location",
    "location_experience",
    "location_education",
    "searching",
    "scoring",
]
ORDER_BY_VALUES = [None, "desc", "asc"]
VALID_EXTENSIONS = [
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".doc",
    ".docx",
    ".rtf",
    ".dotx",
    ".odt",
    ".odp",
    ".ppt",
    ".pptx",
    ".rtf",
    ".msg",
]
INVALID_FILENAME = [".", ".."]


def validate_boolean(name, value):
    """
    This function validates the fact that the value is a boolean. If not, it raises a
    TypeError.
    If the given value is a string that can be converted to a boolean, it converts it.
    :param name: <string> The name of the variable to validate
    :param value: <any> The value to validate
    :return: <boolean> The value
    """
    if not isinstance(value, bool) or (
        isinstance(value, str) and value not in ["0", "1"]
    ):
        raise TypeError(
            "{name} must be boolean not {value}".format(name=name, value=value)
        )

    return value if isinstance(value, bool) else bool(int(value))


def validate_key(obj, value, regex=None):
    if not isinstance(value, str) and value is not None:
        raise TypeError(obj + " key must be string")

    if regex and not bool(re.match(regex, value)):
        raise ValueError(f"{obj} key must match {regex}")

    return value


def validate_value(value, values, message="value"):
    if value not in values:
        raise ValueError("{} must be in {}".format(message, str(values)))
    return value


def validate_reference(value):
    if value is None:
        return value
    if not isinstance(value, str) and value is not None:
        raise TypeError("reference must be string not {}".format(value))

    return value


def validate_page(value):
    if not isinstance(value, int):
        raise TypeError("page must be 'int'")

    return value


def validate_limit(value):
    if not isinstance(value, int):
        raise TypeError("limit must be 'int'")

    return value


def validate_provider_keys(value):
    if not value or not all(isinstance(elt, str) for elt in value):
        raise TypeError("provider_ids must contain list of strings")
    return value


def is_valid_extension(file_path):
    ext = os.path.splitext(file_path)[1]
    if not ext:
        return False
    return ext in VALID_EXTENSIONS or ext.lower() in VALID_EXTENSIONS


def is_valid_filename(file_path):
    name = os.path.basename(file_path)
    return name not in INVALID_FILENAME


def validate_response(response):
    if response.headers["Content-Type"] != "application/json":
        return {
            "code": response.status_code,
            "message": "A generic error occurred on the server",
        }
    return response.json()
