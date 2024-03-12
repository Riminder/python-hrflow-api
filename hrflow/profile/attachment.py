from ..core import format_item_payload
from ..core.rate_limit import rate_limiter
from ..core.validation import validate_response


class ProfileAttachments:
    """Manage documents related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    @rate_limiter
    def list(self, source_key, key=None, reference=None, email=None):
        """
        Retrieve the interpretability information.

        Args:
            source_key:             <string>
                                    source_key
            key:                    <string>
                                    key
            reference:              <string>
                                    profile_reference
            email:                  <string>
                                    profile_email

        Returns
            Attachment information

        """
        query_params = format_item_payload("profile", source_key, key, reference, email)
        response = self.client.get("profile/indexing/attachments", query_params)
        return validate_response(response)
