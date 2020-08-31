class DocumentRevealing():
    """Manage revealing related profile calls."""

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
        response = self.client.post('document/revealing', json=payload)
        return response.json()
