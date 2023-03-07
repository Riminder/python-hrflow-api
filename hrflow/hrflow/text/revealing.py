from ..utils import validate_response


class TextRevealing:
    """Manage revealing related calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def post(self, text):
        """
        Predict missing & likely hard-skills and soft-skills.

        Args:
            text:                   <string>
                                    text
        Returns
            Revealing

        """
        payload = {"text": text}
        response = self.client.post("text/revealing", json=payload)
        return validate_response(response)
