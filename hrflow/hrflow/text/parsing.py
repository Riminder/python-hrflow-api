import typing as t

from ..utils import validate_response


class TextParsing:
    """Manage Text parsing related calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def post(self, texts: t.List[str]) -> t.Dict[str, t.Any]:
        """
        Parse a raw Text. Extract over 50 data point from any raw input text.

        Args:
            texts:      <list[str]>
                        Parse a list of texts. Each text can be: the full text
                        of a Job, a Resume, a Profile, an experience, a Job and more.

        Returns:
            `/text/parsing` response
        """

        payload = dict(texts=texts)

        response = self.client.post("text/parsing", json=payload)

        return validate_response(response)
