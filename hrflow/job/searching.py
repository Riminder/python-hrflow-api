import time

TIMESTAMP_NOW = time.time()


class JobSearching():
    """Manage stage related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def get(self, name=None):
        """
                Search a job by name.

                Args:
                    name:               <string>
                                        name
                Returns
                   Jobs matching the seach
        """
        query_params = {}
        if name:
            query_params['name'] = name
        response = self.client.get("jobs/searching", query_params)
        return response.json()
