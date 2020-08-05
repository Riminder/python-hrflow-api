from ..utils import validate_key, validate_page, validate_limit, validate_order_by, validate_sort_by


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
        query_params["page"] = validate_page(page)
        query_params["limit"] = validate_limit(limit)
        query_params["sort_by"] = sort_by
        query_params["order_by"] = validate_order_by(order_by)
        response = self.client.get("sources", query_params)
        return response.json()

    def get(self, key=None):
        """
            Get source given a source id.

            Args:
                source_key:         <string>
                                    source_key
            Returns
                Source if exists

        """
        query_params = {"source_key": validate_key("Source", key)}
        response = self.client.get('source', query_params)
        return response.json()
