from ..core.rate_limit import rate_limiter
from ..core.validation import validate_response


class TextImaging:
    """Manage Imaging API related calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    @rate_limiter
    def post(self, text, width=256):
        """
        This endpoint allows you to generate an image from a job description text.

        Args:
            text:                   <string>
                                    Job text that describes the image to be generated.
                                    Ideally it should includes a "Job title".
            width:                  <int>
                                    Width of the image to be generated. Default is 256.
                                    (The width and height of the image should be among
                                    the following pixel values : [256, 512, 1024 ])
        Returns
            A public url to the generated image.

        """
        payload = {"text": text, "width": width}
        response = self.client.post("text/imaging", json=payload)
        return validate_response(response)
