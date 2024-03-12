from ..core.rate_limit import rate_limiter
from ..core.validation import (
    ORDER_BY_VALUES,
    validate_key,
    validate_limit,
    validate_page,
    validate_response,
    validate_value,
)


class Board(object):
    def __init__(self, client):
        self.client = client

    @rate_limiter
    def list(self, name=None, page=1, limit=30, sort_by="date", order_by="desc"):
        """
        Search boards for given filters.

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
        query_params["order_by"] = validate_value(order_by, ORDER_BY_VALUES, "order by")
        response = self.client.get("boards", query_params)
        return validate_response(response)

    @rate_limiter
    def get(self, key=None):
        """
        Get source given a board key.

        Args:
            key:         <string>
                         board_key
        Returns
            Board if exists

        """
        query_params = {"key": validate_key("Board", key)}
        response = self.client.get("board", query_params)
        return validate_response(response)
