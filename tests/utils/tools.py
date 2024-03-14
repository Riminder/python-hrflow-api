import io
import os
import typing as t
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv
from pydantic import BaseModel
from pytest import fail, skip

from hrflow import Hrflow

from .schemas import JobIndexingResponse, ProfileIndexingResponse

_env_loaded = False


def _var_from_env_get(varname: str) -> str:
    """
    Gets the value of the specified variable (`varname`) from the environment.

    Args:
        varname (str): The name of the variable to retrieve.

    Returns:
        The value corresponding to `varname` in the environment if found; otherwise,
        the test calling this function will be skipped.
    """

    # this allows to load the environment once
    global _env_loaded
    if not _env_loaded:
        load_dotenv()
        _env_loaded = True

    value = os.environ.get(varname)
    if value is None:
        skip(f"{varname} was not found in the environment")

    return value


def _now_iso8601_get() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")


def _iso8601_to_datetime(datestr: str) -> t.Optional[datetime]:
    try:
        return datetime.fromisoformat(datestr)
    except Exception:
        pass


def _file_get(
    url: str, file_name: t.Optional[str] = None
) -> t.Optional[t.Union[io.BytesIO, io.BufferedReader]]:
    """
    Gets the file corresponding to the specified `url`. If tests/assets/`file_name`
    does not exist, it will be downloaded from `url` and stored for reuse, basically,
    it will be locally cached.

    Args:
        url (str): The download URL of the file.
        file_name (optional[str]): The name to assign to the file.

    Returns:
        The content of the file if it exists; otherwise, returns `None`.
    """

    if file_name is None:  # deduce from the url
        file_name = url[url.rfind("/") + 1 :]

    # look up for its cached version
    dir_path = "tests/assets"
    file_path = os.path.join(dir_path, file_name)
    if os.path.isfile(file_path):
        with open(file_path, "rb") as file:
            file_object = io.BytesIO(file.read())
            file_object.name = file_path
            return file_object

    response = requests.get(url)

    if response.status_code != requests.codes.ok:
        return

    file_data = response.content

    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    # cache the content
    with open(file_path, "wb+") as file:
        file.write(file_data)

    return io.BytesIO(file_data)


def _check_same_keys_equality(source: t.Dict[str, t.Any], target: BaseModel):
    """
    Performs a shallow equality check between the keys at the same levels in the
    dictionaries `source` and `target`.

    Args:
        source (dict): The dictionary from which `target` was derived, using indexing
        or other methods.
        target (BaseModel): The Pydantic response object corresponding to `source`.

    Returns:
        None
    """

    dumped = target.dict()  # easier to compare dict vs dict

    def _fail_message_get(key, source_value, target_value, is_complex=False):
        return (
            f"{'complex' if is_complex else 'primitive'} comparison failed: '{key}' is"
            f" expected to be '{source_value}', got '{target_value}'"
        )

    def _compare(source: t.Dict[str, t.Any], target: t.Dict[str, t.Any]):
        for key in source:

            # compare only the keys that are present in both AND at the same level
            if key not in target:
                continue

            source_value = source[key]
            target_value = target[key]
            source_value_t = type(source_value)
            target_value_t = type(target_value)

            # type comparison
            if source_value_t != target_value_t:
                fail(
                    f"'{key}' expected to be of type '{source_value_t}', got"
                    f" '{target_value_t}'"
                )

            # list vs list comparison
            # lists are expected to be homogenous
            # if list type is dict, each item will be compared with a recursive call
            # otherwise, perform basic python comparison ==
            elif isinstance(source_value, list):

                # both lists must be of same size
                assert len(source_value) == len(target_value) or fail(
                    f"'{key}' is expected to be of length {len(source_value)}, but it"
                    f" is {len(target_value)}"
                )

                if len(source_value) == 0:
                    continue

                if isinstance(source_value[0], dict):
                    for ii in range(len(source_value)):
                        _compare(source_value[ii], target_value[ii])
                else:  # basic python comparisong should be enough
                    assert source_value == target_value or fail(
                        _fail_message_get(
                            key, source_value, target_value, is_complex=True
                        )
                    )

            # recursive call
            elif isinstance(source_value, dict):
                _compare(source_value, target_value)

            # basic python comparison for primitive types
            else:
                assert source_value == target_value or fail(
                    _fail_message_get(key, source_value, target_value, is_complex=False)
                )

    _compare(source, dumped)


def _indexed_response_get(
    hf: Hrflow, holder_key: str, json: t.Dict[str, t.Any]
) -> t.Union[JobIndexingResponse, ProfileIndexingResponse]:
    """
    Abstract function for indexing one-time jobs (or profiles). This function is
    primarily used to avoid dependencies on specific object keys when performing
    tasks such as archiving or editing.

    Args:
        hf (Hrflow): The Hrflow API class.
        holder_key (str): The key of the board (or source).
        json (dict): The JSON object of the job (or source).

    Returns:
        The response Pydantic class.
    """

    is_job = "info" not in json

    model = (JobIndexingResponse if is_job else ProfileIndexingResponse).parse_obj(
        getattr(hf, "job" if is_job else "profile").storing.add_json(holder_key, json)
    )

    assert (
        model.code == requests.codes.created
    ), f"{model.code=} != {requests.codes.created=}, {model.message=}"

    return model
