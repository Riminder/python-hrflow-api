import json
from ..utils import format_item_payload, validate_key, validate_response, validate_reference


class JobIndexing:
    """Manage parsing related job calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def add_json(self, board_key, job_json):
        """Use the api to add a new profile using profile_data."""
        job_json['board_key'] = validate_key("Board", board_key)
        response = self.client.post("job/indexing", json=job_json)
        return validate_response(response)

    def edit(self, board_key, key, reference=None, job_json=None):
        """
        Retrieve the parsing information.

        Args:
            board_key:              <string>
                                    board id
            key:                    <string>
                                    job id
            reference:              <string>
                                    job_reference
            job_json:               <string>
                                    job json

        Returns
            parsing information

        """
        if job_json is None:
            job_json = {}

        job_json['board_key'] = validate_key("Board", board_key)
        job_json['key'] = validate_key("Job", key)

        if reference:
            job_json['reference'] = validate_reference(reference)
        """Use the api to add a new profile using profile_data."""
        response = self.client.put("job/indexing", json=job_json)
        return validate_response(response)

    def get(self, board_key, key=None, reference=None):
        """
        Retrieve the parsing information.

        Args:
            board_key:              <string>
                                    board id
            key:                    <string>
                                    job id
            reference:              <string>
                                    job_reference

        Returns
            parsing information

        """
        query_params = format_item_payload('job', board_key, key, reference)
        response = self.client.get('job/indexing', query_params)
        return validate_response(response)

    def archive(self, board_key, key=None, reference=None):
        """
        Archive Job

        Args:
            board_key:              <string>
                                    board id
            key:                    <string>
                                    job id
            reference:              <string>
                                    job_reference
        Returns
            archive job

        """
        payload = format_item_payload('job', board_key, key, reference)
        response = self.client.patch("job/indexing/archive", json=payload)
        return validate_response(response)
