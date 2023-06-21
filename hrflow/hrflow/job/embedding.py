from ..utils import format_item_payload, validate_response


class JobEmbedding:
    """Manage embedding related job calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

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
        query_params = format_item_payload("job", board_key, key, reference)
        response = self.client.get("job/embedding", query_params)
        return validate_response(response)
