import os

from .validation import (
    is_valid_extension,
    is_valid_filename,
    validate_key,
    validate_reference,
)


def format_item_payload(item, provider_key, key, reference=None, email=None):
    provider = "source_key" if item == "profile" else "board_key"

    payload = {provider: validate_key("provider", provider_key)}
    if key:
        payload["key"] = validate_key("item", key)
    if reference:
        payload["reference"] = validate_reference(reference)
    if email:
        payload["profile_email"] = email

    return payload


def get_files_from_dir(dir_path, is_recurcive):
    file_res = []
    files_path = os.listdir(dir_path)

    for file_path in files_path:
        true_path = os.path.join(dir_path, file_path)
        if os.path.isdir(true_path) and is_recurcive:
            if is_valid_filename(true_path):
                file_res += get_files_from_dir(true_path, is_recurcive)
            continue
        if is_valid_extension(true_path):
            file_res.append(true_path)
    return file_res
