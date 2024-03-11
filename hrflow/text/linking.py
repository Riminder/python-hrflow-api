from ..core.rate_limit import rate_limiter
from ..core.validation import validate_response


class TextLinking:
    """Manage Text linking calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    @rate_limiter
    def post(self, word, top_n=5):
        """
        Find synonyms or the top N most similar words to a word.

        Args:
            text:                   <string>
                                    text
            top_n:                  <string>
                                    top_n
        Returns
            Find synonyms or the top N most similar words to a word.
        """
        payload = {"word": word, "top_n": top_n}
        response = self.client.post("text/linking", json=payload)
        return validate_response(response)
