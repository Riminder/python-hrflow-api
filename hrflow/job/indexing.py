from ..utils import get_item, validate_key


class JobIndexing():
    """Manage parsing related job calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def add_json(self, board_key, job_json):
        """Use the api to add a new profile using profile_data."""
        job_json['board_key'] = validate_key("Board", board_key)
        response = self.client.post("job/indexing", json=job_json)
        return response.json()

    def edit(self, board_key, key, job_json):
        job_json['board_key'] = validate_key("Board", board_key)
        job_json['key'] = validate_key("Job", key)
        """Use the api to add a new profile using profile_data."""
        response = self.client.put("job/indexing", json=job_json)
        return response.json()

    def get(self, board_key, key, reference=None):
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
        query_params = get_item('job', board_key, key, reference)
        response = self.client.get('job/indexing', query_params)
        return response.json()
