from ..utils import validate_response


class DocumentLinking():
    """Manage parsing related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def post(self, text, top_n=5):
        """
        Retrieve revealing.

        Args:
            text:                   <string>
                                    text
            top_n:                  <string>
                                    top_n
        Returns
            Revealing

        """
        payload = {
            "text": text,
            "top_n": top_n
        }
        response = self.client.post('document/linking', json=payload)
        return validate_response(response)
