from ..utils import validate_response


class TextParsing:
    """Manage Text parsing related calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def post(self, text):
        """
        Extract over 50 data point from any raw input text.

        Args:
            text:                   <string>
                                    text
        Returns
            Parsed entities from the text.

        """
        payload = {"text": text}
        response = self.client.post("text/parsing", json=payload)
        return validate_response(response)
