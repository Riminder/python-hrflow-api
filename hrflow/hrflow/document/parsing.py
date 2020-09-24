from ..utils import validate_response


class DocumentParsing():
    """Manage parsing related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def post(self, text):
        """
        Retrieve revealing.

        Args:
            text:                   <string>
                                    text
        Returns
            Revealing

        """
        payload = {
            "text": text
        }
        response = self.client.post('document/parsing', json=payload)
        return validate_response(response)
