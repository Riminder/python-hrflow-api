

class Filter(object):

    def __init__(self, client):
        self.client = client

    def list(self):
        response = self.client.get("filters")
        return response.json()

    def get(self, filter_id=None, filter_reference=None):
        query_params = {}
        if filter_id:
            query_params["filter_id"] = self._validate_id(filter_id, 'filter_id')
        if filter_reference:
            query_params["filter_reference"] = self._validate_id(filter_reference, 'filter_reference')

        response = self.client.get('filter', query_params)
        return response.json()

    def _validate_id(self, value, field_name=''):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{} must be string".format(field_name))

        return value
