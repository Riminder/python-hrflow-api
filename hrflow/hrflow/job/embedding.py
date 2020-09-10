from ..utils import get_item


class JobEmbedding():
    """Manage embedding related job calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

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
        response = self.client.get('job/embedding', query_params)
        return response.json()
