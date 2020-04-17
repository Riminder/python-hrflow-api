from .validator import validate_source_ids, validate_profile_id, validate_profile_reference


class ProfileTags():
    """Manage Tags related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def list(self, source_id=None, profile_id=None, profile_reference=None):
        """
        Retrieve Profile's tags.

        Args:
            source_id:              <string>
                                    source id
            profile_id:             <string>
                                    profile id
            profile_reference:      <string>
                                    profile_reference
        Returns
            document information, like type, name, extension, url.. associated to the profile id

        """
        query_params = {"source_id": validate_source_ids(source_id)}
        if profile_id:
            query_params["profile_id"] = validate_profile_id(profile_id)
        if profile_reference:
            query_params["profile_reference"] = validate_profile_reference(profile_reference)
        response = self.client.get('profile/tags', query_params)
        return response.json()
