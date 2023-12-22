from ..utils import format_item_payload, validate_response


class ProfileRevealing:
    """Manage revealing related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def get(self, source_key=None, key=None, reference=None, email=None):
        """
        Retrieve Parsing information.

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
            Get information

        """
        query_params = format_item_payload("profile", source_key, key, reference, email)
        response = self.client.get("profile/revealing", query_params)
        return validate_response(response)
