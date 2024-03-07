import pytest
from requests import codes as http_codes

from hrflow import Hrflow

from .utils.schemas import AuthResponse
from .utils.tools import _var_from_env_get


@pytest.mark.auth
def test_valid_all():
    model = AuthResponse.parse_obj(
        Hrflow(
            api_secret=_var_from_env_get("HRFLOW_API_KEY"),
            api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
        ).auth.get()
    )
    assert model.code == http_codes.ok


@pytest.mark.auth
def test_valid_read():
    model = AuthResponse.parse_obj(
        Hrflow(
            api_secret=_var_from_env_get("HRFLOW_API_KEY_READ"),
            api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
        ).auth.get()
    )
    assert model.code == http_codes.ok


@pytest.mark.skip(
    reason="write permission key, for now, can not be used for a GET request"
)
@pytest.mark.auth
def test_valid_write():
    model = AuthResponse.parse_obj(
        Hrflow(
            api_secret=_var_from_env_get("HRFLOW_API_KEY_WRITE"),
            api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
        ).auth.get()
    )
    assert model.code == http_codes.ok


# All the keys below, in raw text, are mock


@pytest.mark.auth
def test_invalid_valid_askw():
    model = AuthResponse.parse_obj(
        Hrflow(
            api_secret="askw_d86bb249fff3ac66765f04d43c611675",
            api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
        ).auth.get()
    )
    assert model.code == http_codes.unauthorized


@pytest.mark.auth
def test_api_secret_regex_42():
    with pytest.raises(ValueError):
        Hrflow(
            api_secret="42", api_user=_var_from_env_get("HRFLOW_USER_EMAIL")
        ).auth.get()


@pytest.mark.auth
def test_api_secret_regex_not_hex():
    with pytest.raises(ValueError):
        Hrflow(
            api_secret="ask_xa62249b693f2b4cc29524624abfc659",
            api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
        ).auth.get()


@pytest.mark.auth
def test_api_secret_regex_basic_key():
    with pytest.raises(ValueError):
        Hrflow(
            api_secret="b2631028fab36393d8bf05ca143b75e3424ea78e",
            api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
        ).auth.get()


@pytest.mark.auth
def test_api_secret_regex_valid_with_padding_start():
    with pytest.raises(ValueError):
        Hrflow(
            api_secret=" ask_d89a3523b8b5c34b24e8831239bb6ba0",
            api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
        ).auth.get()


@pytest.mark.auth
def test_api_secret_regex_valid_with_padding_end():
    with pytest.raises(ValueError):
        Hrflow(
            api_secret="ask_7f24675fbaadfaeb1e9ea57201b1b92c ",
            api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
        ).auth.get()


@pytest.mark.auth
def test_api_secret_too_short():
    with pytest.raises(ValueError):
        Hrflow(
            api_secret=_var_from_env_get("HRFLOW_API_KEY")[:-1],
            api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
        ).auth.get()


@pytest.mark.auth
def test_api_secret_too_long():
    with pytest.raises(ValueError):
        Hrflow(
            api_secret=_var_from_env_get("HRFLOW_API_KEY") + "f",
            api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
        ).auth.get()
