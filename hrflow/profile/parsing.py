import os
import json

from ..utils import get_item, validate_key, validate_reference, get_files_from_dir


class ProfileParsing():
    """Manage parsing related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def add(self, source_key, key=None, profile_file=None, profile_content_type=None, reference=None, created_at=None,
            labels=[], tags=[], metadatas=[], sync_parsing=0, sync_parsing_indexing=1, webhook_parsing_sending=0):
        """
        Add a profile resume to a sourced key.

        Args:
            source_key:              <string>
                                     source_key
            key                      <string>
                                     source_key
            profile_file:            <binary>
                                     profile binary
            profile_content_type     <string>
                                     file content type
            reference:               <string> (default to None)
                                     reference to assign to the profile
            created_at:              <string>
                                     original date of the application of the profile as ISO format
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
            'source_key': validate_key("Source", source_key),
            'key': validate_key("profile", key),
            'profile_content_type': profile_content_type,
            'reference': validate_reference(reference),
            'created_at': created_at,
            'labels': json.dumps(labels),
            'tags': json.dumps(tags),
            'metadatas': json.dumps(metadatas),
            'sync_parsing': sync_parsing,
            'sync_parsing_indexing': sync_parsing_indexing,
            'webhook_parsing_sending': webhook_parsing_sending
        }
        response = self.client.post("profile/parsing/file", data=payload, files={"file": profile_file})
        return response.json()

    def add_folder(self, source_key, dir_path, is_recurcive=False, created_at=None, sync_parsing=0):
        """Add all profile from a given directory."""
        if not os.path.isdir(dir_path):
            raise ValueError(dir_path + ' is not a directory')
        files_to_send = get_files_from_dir(dir_path, is_recurcive)
        succeed_upload = {}
        failed_upload = {}
        for file_path in files_to_send:
            try:
                with open(file_path) as f:
                    profile_file = f.read()
                resp = self.add(source_key=source_key, profile_file=profile_file, created_at=created_at,
                                sync_parsing=sync_parsing)
                if resp['code'] != 200 and resp['code'] != 201:
                    failed_upload[file_path] = ValueError('Invalid response: ' + str(resp))
                else:
                    succeed_upload[file_path] = resp
            except BaseException as e:
                failed_upload[file_path] = e
        result = {
            'success': succeed_upload,
            'fail': failed_upload
        }
        return result

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
        query_params = get_item("profile", source_key, key, reference, email)
        response = self.client.get('profile/parsing', query_params)
        return response.json()
