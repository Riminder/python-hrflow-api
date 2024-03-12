from ..core.rate_limit import rate_limiter
from ..core.validation import validate_response


class TextEmbedding:
    """Manage embedding related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    @rate_limiter
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
