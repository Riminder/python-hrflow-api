import typing as t

from ..core.rate_limit import rate_limiter
from ..core.validation import validate_response


class TextParsing:
    """Manage Text parsing related calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    @rate_limiter
    def post(
        self, text: t.Optional[str] = None, texts: t.Optional[t.List[str]] = None
    ) -> t.Dict[str, t.Any]:
        """
        Parse a raw Text. Extract over 50 data point from any raw input text.

        Args:
            texts:      <list[str]>
                        Parse a list of texts. Each text can be: the full text
                        of a Job, a Resume, a Profile, an experience, a Job and more.

        Returns:
            `/text/parsing` response
        """

        if text is not None:
            if texts is not None:
                raise ValueError("Only one of text or texts must be provided.")
            else:
                payload = dict(text=text)
        else:
            if texts is None:
                raise ValueError("Either text or texts must be provided.")
            else:
                payload = dict(texts=texts)

        response = self.client.post("text/parsing", json=payload)

        return validate_response(response)
