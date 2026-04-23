import typing as t

from ..core.rate_limit import rate_limiter
from ..core.validation import validate_response


class TextGeocoding:
    """Manage geocoding related calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    @rate_limiter
    def post(
        self,
        texts: t.List[str],
    ) -> t.Dict[str, t.Any]:
        """
        Geocode a list of texts.

        Args:
            texts:              <list[str]>
                    Geocode a list of texts. Example: ["112 avenue charles de gaulle 92200 neuilly-sur-seine", "New York", "7 rue 4 septembre Paris"].

        Returns:
            `/text/geocoding` response
        """
        payload = dict(
            texts=texts,
        )

        response = self.client.post("text/geocoding", json=payload)
        return validate_response(response)