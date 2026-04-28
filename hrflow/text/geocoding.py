import typing as t

from ..core.rate_limit import rate_limiter
from ..core.validation import validate_response


class TextGeocoding:
    """Manage text geocoding calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    @rate_limiter
    def post(self, text: str) -> t.Dict[str, t.Any]:
        """
        Geocode a location text. Retrieve geojson data for a textual location
        input.
        (https://api.hrflow.ai/v1/text/geocoding).

        Args:
            text:               <string>
                                The location text to geocode.

        Returns:
            Geojson data for the given location text.
        """
        payload = {"text": text}
        response = self.client.post("text/geocoding", json=payload)
        return validate_response(response)
