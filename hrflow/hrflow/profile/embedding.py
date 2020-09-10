import json

from ..utils import get_item


class ProfileEmbedding():
    """Manage embedding related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def get(self, source_key, key, reference=None, email=None, fields={}):
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
            fields:                 json object
                                    fields

        Returns
            interpretability information

        """
        query_params = get_item("profile", source_key, key, reference, email)
        if fields:
            query_params["fields"] = json.dumps(fields)
        response = self.client.get('profile/embedding', query_params)
        return response.json()
