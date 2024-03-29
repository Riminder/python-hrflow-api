import json

from ..core.rate_limit import rate_limiter
from ..core.validation import (
    ORDER_BY_VALUES,
    SORT_BY_VALUES,
    STAGE_VALUES,
    validate_limit,
    validate_page,
    validate_provider_keys,
    validate_response,
    validate_value,
)


class ProfileSearching:
    """Manage stage related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    @rate_limiter
    def list(
        self,
        source_keys=None,
        stage=None,
        page=1,
        limit=30,
        sort_by="created_at",
        order_by=None,
        **kwargs,
    ):
        """
        Retrieve the scoring information.

        Args:
            source_keys:        <list>
                                source_keys
            stage:              <string>
                                stage
            limit:              <int> (default to 30)
                                number of fetched profiles/page
            page:               <int> REQUIRED default to 1
                                number of the page associated to the pagination
            sort_by:            <string>
            order_by:           <string>

        Returns
            parsing information

        """

        query_params = {
            "source_keys": json.dumps(validate_provider_keys(source_keys)),
            "stage": validate_value(stage, STAGE_VALUES, "stage"),
            "limit": validate_limit(limit),
            "page": validate_page(page),
            "sort_by": validate_value(sort_by, SORT_BY_VALUES, "sort by"),
            "order_by": validate_value(order_by, ORDER_BY_VALUES, "oder by"),
        }

        params = {**query_params, **kwargs}
        response = self.client.get("profiles/searching", params)
        return validate_response(response)
