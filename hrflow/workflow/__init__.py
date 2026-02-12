from ..core.rate_limit import rate_limiter
from ..core.validation import (
    ORDER_BY_VALUES,
    validate_limit,
    validate_page,
    validate_response,
    validate_value,
)


class Workflow(object):
    def __init__(self, client):
        self.client = client

    @rate_limiter
    def list(
        self, name=None, environment=None, page=1, limit=30, order_by="desc"
    ):
        """
        Find Workflows in a Workspace.
        (https://api.hrflow.ai/v1/workflows).

        Args:
            name:               <string>
                                (Optional) The Workflow name. If empty, the API
                                will return all possible values.
            environment:        <string>
                                (Optional) The deployment context (production,
                                staging, test). Returns all values if omitted.
            page:               <integer> (default to 1)
                                API page offset.
            limit:              <integer> (default to 30)
                                Number of entities per page.
            order_by:           <string> (default to "desc")
                                Order results by creation date: "asc" or "desc".

        Returns:
            List of workflows matching the given filters.
        """
        query_params = {}
        if name:
            query_params["name"] = name
        if environment:
            query_params["environment"] = environment
        query_params["page"] = validate_page(page)
        query_params["limit"] = validate_limit(limit)
        query_params["order_by"] = validate_value(
            order_by, ORDER_BY_VALUES, "order by"
        )
        response = self.client.get("workflows", query_params)
        return validate_response(response)
