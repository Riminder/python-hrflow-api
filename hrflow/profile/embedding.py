import json
from .validator import validate_source_id, validate_profile_id, validate_profile_reference, format_fields


class ProfileEmbedding():
    """Manage embedding related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def get(self, source_id, profile_id, profile_reference=None, profile_email=None, fields={}):
        """
        Retrieve the interpretability information.

        Args:
            source_id:              <string>
                                    source id
            profile_id:             <string>
                                    profile id
            profile_reference:      <string>
                                    profile_reference
            profile_email:          <string>
                                    profile_email
            fields:                 json object
                                    fields

        Returns
            interpretability information

        """
        query_params = {}
        query_params["source_id"] = validate_source_id(source_id)
        if profile_id:
            query_params["profile_id"] = validate_profile_id(profile_id)
        if profile_reference:
            query_params["profile_reference"] = validate_profile_reference(profile_reference)
        if profile_email:
            query_params["profile_email"] = profile_email
        if fields:
            query_params["fields"] = json.dumps(fields)
        response = self.client.get('profile/embedding', query_params)
        return response.json()
