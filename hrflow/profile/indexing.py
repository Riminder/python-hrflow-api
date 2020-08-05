from ..utils import get_item


class ProfileIndexing():
    """Manage embedding related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def add(self, profile_json):
        """Use the api to add a new profile using profile_data."""
        response = self.client.post("profile/indexing", json=profile_json)
        return response.json()

    def put(self, profile_json):
        """Use the api to add a new profile using profile_data."""
        response = self.client.put("profile/indexing", json=profile_json)
        return response.json()

    def get(self, source_key, key, reference=None, email=None):
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
            Get information

        """
        query_params = get_item('profile', source_key, key, reference, email)
        response = self.client.get('profile/indexing', query_params)
        return response.json()
