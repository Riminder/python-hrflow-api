import json

from ..core.rate_limit import rate_limiter
from ..core.validation import (
    ORDER_BY_VALUES,
    SORT_BY_VALUES,
    STAGE_VALUES,
    validate_key,
    validate_limit,
    validate_page,
    validate_provider_keys,
    validate_response,
    validate_value,
)


class ProfileScoring:
    """Manage stage related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    @rate_limiter
    def list(
        self,
        source_keys=None,
        board_key=None,
        job_key=None,
        use_agent=1,
        agent_key=None,
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
            board_key:          <string>
                                board_key
            job_key:            <string>
                                job_key
            use_agent:          <int>
                                use_agent
            agent_key:            <string>
                                agent_key
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
            "board_key": validate_key("Board", board_key),
            "job_key": validate_key("Job", job_key),
            "use_agent": use_agent,
            "agent_key": validate_key("Agent", agent_key),
            "stage": validate_value(stage, STAGE_VALUES, "stage"),
            "limit": validate_limit(limit),
            "page": validate_page(page),
            "sort_by": validate_value(sort_by, SORT_BY_VALUES, "sort by"),
            "order_by": validate_value(order_by, ORDER_BY_VALUES, "order by"),
        }

        params = {**query_params, **kwargs}
        response = self.client.get("profiles/scoring", params)
        return validate_response(response)
