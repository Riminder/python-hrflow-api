"""Profile related calls."""
import json
from .feedback import ProfileFeedback
from .attachment import ProfileAttachments
from .tag import ProfileTags
from .metadata import ProfileMetadatas
from .parsing import ProfileParsing
from .revealing import ProfileRevealing
from .embedding import ProfileEmbedding
from .searching import ProfileSearching
from .scoring import ProfileScoring
from .reasoning import ProfileReasoning

from .validator import *


class Profile(object):
    """
    Class that interacts with hrflow API profiles endpoint.

    Usage example:

    >>> from hrflow import client
    >>> from hrflow.profile import Profile
    >>> client = client(api_key="YOUR_API_KEY")
    >>> profile = Profile(self.client)
    >>> result = profile.get_profiles(source_ids=["5823bc959983f7a5925a5356020e60d605e8c9b5"])
    >>> print(result)
    {
        "code": 200,
        "message": "OK",
        "data": {
            "page": 1,
            "maxPage": 3,
            "count_profiles": 85,
            "profiles": [
            {
                "profile_id": "215de6cb5099f4895149ec0a6ac91be94ffdd246",
                "profile_reference": "49583",
                ...
    """

    def __init__(self, client):
        """
        Initialize Profile object with hrflow client.

        Args:
            client: hrflow client instance <hrflow object>

        Returns
            Profile instance object.

        """
        self.client = client
        self.feedback = ProfileFeedback(self.client)
        self.attachment = ProfileAttachments(self.client)
        self.tag = ProfileTags(self.client)
        self.metadata = ProfileMetadatas(self.client)
        self.parsing = ProfileParsing(self.client)
        self.revealing = ProfileRevealing(self.client)
        self.embedding = ProfileEmbedding(self.client)
        self.searching = ProfileSearching(self.client)
        self.scoring = ProfileScoring(self.client)
        self.reasoning = ProfileReasoning(self.client)

    def add_json(self, source_id, profile_json, profile_reference=None, profile_labels=[], profile_tags=[],
                 profile_metadatas=[], timestamp_reception=None):
        """Use the api to add a new profile using profile_data."""
        payload = {
            'source_id': validate_source_id(source_id),
            'profile_type': 'json',
            'profile_reference': validate_profile_reference(profile_reference),
            'profile_labels': json.dumps(profile_labels),
            'profile_tags': json.dumps(profile_tags),
            'profile_metadatas': json.dumps(profile_metadatas),
            'profile_json': json.dumps(profile_json)
        }
        # some enrichement for profile_json
        if timestamp_reception is not None:
            payload['timestamp_reception'] = validate_timestamp(timestamp_reception, 'timestamp_reception')

        response = self.client.post("profile", data=payload)
        return response.json()

    def add_file(self, source_id, profile_file, profile_content_type=None, profile_reference=None, profile_labels=[],
                 profile_tags=[], profile_metadatas=[], sync_parsing=0, timestamp_reception=None):
        """
        Add a profile resume to a sourced id.

        Args:
            source_id:              <string>
                                    source id
            profile_file:           <binary>
                                    profile binary
            profile_content_type    <string>
                                    file content type
            profile_reference:      <string> (default to "")
                                    reference to assign to the profile
            profile_labels:         <dict>
                                    profile's label
            profile_tags:         <dict>
                                    profile's tag
            profile_metadatas:      <dict>
                                    profile's metadatas
            sync_parsing            <bool>
                                    0 or 1
            timestamp_reception:    <int>
                                    original date of the application of the profile

        Returns
            Response that contains code 201 if successful
            Other status codes otherwise.

        """
        payload = {
            'source_id': validate_source_id(source_id),
            'profile_type': 'file',
            'profile_content_type': profile_content_type,
            'profile_reference': validate_profile_reference(profile_reference),
            'profile_labels': json.dumps(profile_labels),
            'profile_tags': json.dumps(profile_tags),
            'profile_metadatas': json.dumps(profile_metadatas),
            'sync_parsing': sync_parsing
        }
        # some enrichement for profile_
        if timestamp_reception is not None:
            payload['timestamp_reception'] = validate_timestamp(timestamp_reception, 'timestamp_reception')

        response = self.client.post("profile", data=payload, files={"file": profile_file})
        return response.json()

    def add_folder(self, source_id, dir_path, is_recurcive=False, timestamp_reception=None, sync_parsing=0):
        """Add all profile from a given directory."""
        if not os.path.isdir(dir_path):
            raise ValueError(dir_path + ' is not a directory')
        files_to_send = get_files_from_dir(dir_path, is_recurcive)
        succeed_upload = {}
        failed_upload = {}
        for file_path in files_to_send:
            try:
                resp = self.add_file(source_id=source_id,
                                     file_path=file_path, profile_reference="",
                                     timestamp_reception=timestamp_reception, sync_parsing=sync_parsing)
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
