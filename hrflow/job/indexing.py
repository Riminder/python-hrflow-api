from ..utils import get_item


class JobIndexing():
    """Manage parsing related job calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def add(self, job_json):
        """Use the api to add a new profile using profile_data."""
        response = self.client.post("job/indexing", json=job_json)
        return response.json()

    def put(self, job_json):
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
