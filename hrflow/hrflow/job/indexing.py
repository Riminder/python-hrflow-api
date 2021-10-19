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

    def edit(self, board_key, key=None, job_json=None):
        """
        This method allows to edit a job
        in HrFlow.ai. 
        The job can be edited either through its key (passed as an argument) or its reference 
        which is a field in the job_json,
        at least one of the two values must be provided.
        Args:
            board_key:              <string>
                                    board id
            key:                    <string>
                                    job id
            job_json:               <string>
                                    job json structure must follows the structure here https://developers.hrflow.ai/hr-json/job-objects/job-object

        Returns
            Edit the job in the board with the specified identifier

        """
        if job_json is None:
            job_json = {}

        job_json['board_key'] = validate_key("Board", board_key)
        if key:
            job_json['key'] = validate_key("Job", key)
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

    def archive(self, board_key, key=None, reference=None, is_archive=1):
        """
        This method allows to archive (is_archive=1) or unarchive (is_archive=0) a job
        in HrFlow.ai. 
        The job is identified by either its key or its reference,
        at least one of the two values must be provided.

        Args:
            board_key:             <string>
                                    board identifier
            key:                    <string>
                                    job identifier (key)
            reference:              <string>
                                    job identifier (reference)
            is_archive:             <integer> 
                                    default = 1
                                    {0, 1} to indicate archive/unarchive action

        Returns
            Archive/unarchive job response 

        """        
        payload = format_item_payload('job', board_key, key, reference)
        payload["is_archive"] = is_archive
        response = self.client.patch("job/indexing/archive", json=payload)
        return validate_response(response)
