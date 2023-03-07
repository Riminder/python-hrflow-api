from ..utils import validate_response


class TextEmbedding:
    """Manage embedding related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def post(self, text):
        """
        This endpoint allows you to vectorize a Text.



        Args:
            text : <string>
                The text to vectorize.
        Returns
            Embedding vector of the text.

        """
        payload = {
            "text": text,
        }
        response = self.client.post("text/embedding", json=payload)

        return validate_response(response)
