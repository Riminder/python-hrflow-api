import json
import os
import shutil
import uuid

from tqdm import tqdm

from ..core import format_item_payload, get_files_from_dir
from ..core.rate_limit import rate_limiter
from ..core.validation import validate_key, validate_reference, validate_response


class ProfileParsing:
    """Manage parsing related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    @rate_limiter
    def add_file(
        self,
        source_key,
        key=None,
        profile_file=None,
        profile_file_name=None,
        profile_content_type=None,
        reference=None,
        created_at=None,
        labels=[],
        tags=[],
        metadatas=[],
        sync_parsing=0,
        sync_parsing_indexing=1,
        webhook_parsing_sending=0,
    ):
        """
        Add a profile resume to a sourced key.

        Args:
            source_key:              <string>
                                     source_key
            key                      <string>
                                     source_key
            profile_file:            <binary>
                                     profile binary
            profile_file_name:       <string>
                                     file name
            profile_content_type     <string>
                                     file content type
            reference:       <string> (default to None)
                                     reference to assign to the profile
            created_at:              <string>
                                     original date of the application of the
                                     profile as ISO format
            labels:                  <list>
                                     profile's label
            tags:                    <list>
                                     profile's tag
            metadatas:               <list>
                                     profile's metadatas
            sync_parsing             <bool>
                                     0 or 1
            sync_parsing_indexing    <bool>
                                     0 or 1
            webhook_parsing_sending  <bool>
                                     0 or 1

        Returns
            Response that contains code 201 if successful
            Other status codes otherwise.

        """
        payload = {
            "source_key": validate_key("Source", source_key),
            "key": validate_key("profile", key),
            "profile_content_type": profile_content_type,
            "reference": validate_reference(reference),
            "created_at": created_at,
            "labels": json.dumps(labels),
            "tags": json.dumps(tags),
            "metadatas": json.dumps(metadatas),
            "sync_parsing": sync_parsing,
            "sync_parsing_indexing": sync_parsing_indexing,
            "webhook_parsing_sending": webhook_parsing_sending,
        }

        if profile_file_name is None:
            file_payload = {"file": profile_file}
        else:
            file_payload = {"file": (profile_file_name, profile_file)}

        response = self.client.post(
            "profile/parsing/file", data=payload, files=file_payload
        )
        return validate_response(response)

    @rate_limiter
    def add_folder(
        self,
        source_key,
        dir_path,
        is_recurcive=False,
        created_at=None,
        sync_parsing=0,
        move_failure_to=None,
        show_progress=False,
        **kwargs,
    ):
        """
        Parse a folder of profile resumes to a sourced key.

        This method will parse the files in the folder, with the authorized extensions,
        not the subfolders by default.
        If you want to parse the subfolders, set is_recurcive to True.

        Args:
            source_key:              <string>
                                     source_key
            dir_path:                <string>
                                     directory path
            is_recurcive:            <bool>
                                     True or False
            created_at:              <string>
                                     original date of the application of the
                                     profile as ISO format
            sync_parsing             <bool>
                                     0 or 1
            move_failure_to          <string | None>
                                     directory path to move the failed files.
                                     If None, the failed files will not be moved.
            show_progress            <bool>
                                     Show the progress bar
            **kwargs:                <**kwargs>
                                     additional parameters to pass to the parsing API
        """
        if not os.path.isdir(dir_path):
            raise ValueError(dir_path + " is not a directory")
        files_to_send = get_files_from_dir(dir_path, is_recurcive)
        succeed_upload = {}
        failed_upload = {}
        if show_progress:
            files_to_send = tqdm(files_to_send, "Parsing")
        for file_path in files_to_send:
            filename = os.path.basename(file_path)
            try:
                with open(file_path, "rb") as file:
                    resp = self.add_file(
                        source_key=source_key,
                        profile_file=file,
                        profile_file_name=filename,
                        created_at=created_at,
                        sync_parsing=sync_parsing,
                        **kwargs,
                    )
                response_code = str(resp["code"])  # 200, 201, 202, 400, ...
                if response_code[0] != "2":
                    failed_upload[file_path] = ValueError(
                        "Invalid response: " + str(resp)
                    )
                    if move_failure_to is not None:
                        move_to_failed_dir(file_path, move_failure_to)
                else:
                    succeed_upload[file_path] = resp
            except Exception as e:
                failed_upload[file_path] = e
                if move_failure_to is not None:
                    move_to_failed_dir(file_path, move_failure_to)

        result = {"success": succeed_upload, "fail": failed_upload}
        return result

    @rate_limiter
    def get(self, source_key=None, key=None, reference=None, email=None):
        """
        Retrieve Parsing information.

        Args:
            source_key:             <string>
                                    source_key
            key:                    <string>
                                    key
            reference:              <string>
                                    profile_reference
            email:                  <string>
                                    profile_email

        Returns
            Get information

        """
        query_params = format_item_payload("profile", source_key, key, reference, email)
        response = self.client.get("profile/parsing", query_params)
        return validate_response(response)


def move_to_failed_dir(file_path: str, move_failure_to: str):
    file_name = os.path.basename(file_path)
    unique_id = str(uuid.uuid4())

    destination_path = os.path.join(move_failure_to, file_name)
    if os.path.exists(destination_path):
        destination_path = os.path.join(
            move_failure_to, f"same-file-name-{unique_id}_{file_name}"
        )

    shutil.copyfile(file_path, destination_path)
