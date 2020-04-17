class Source(object):

    def __init__(self, client):
        self.client = client

    def list(self, name=None, page=1, limit=30, sort_by='date', order_by='desc'):
        """
            Search sources for given filters.

            Args:
                name:             <string>
                                  name
                page:             <integer>
                                  page
                limit:            <integer>
                                  limit
                sort_by:          <string>
                                  sort_by
                order_by:         <string>
                                  order_by

            Returns
                Result of source's search

        """
        query_params = {}
        if name:
            query_params["name"] = name
        query_params["page"] = page
        query_params["limit"] = limit
        query_params["sort_by"] = sort_by
        query_params["order_by"] = order_by
        response = self.client.get("sources", query_params)
        return response.json()

    def get(self, source_id=None):
        """
            Get source given a source id.

            Args:
                source_id:          <string>
                                    source id
            Returns
                Source if exists

        """
        query_params = {}
        query_params["source_id"] = self._validate_source_id(source_id)
        response = self.client.get('source', query_params)
        return response.json()

    @staticmethod
    def _validate_source_id(value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("source_id must be string")

        return value