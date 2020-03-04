
class Source(object):

    def __init__(self, client):
        self.client = client

    def list(self):
        response = self.client.get("sources")
        return response.json()

    def get(self, source_id=None):
        query_params = {}
        query_params["source_id"] = self._validate_source_id(source_id)

        response = self.client.get('source', query_params)
        return response.json()

    def _validate_source_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("source_id must be string")

        return value
