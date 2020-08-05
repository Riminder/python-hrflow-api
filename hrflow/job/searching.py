import json

from ..utils import validate_provider_keys, validate_stage, validate_limit, validate_page, validate_sort_by, \
    validate_order_by


class JobSearching():
    """Manage stage related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def get(self, board_keys=None, stage=None, page=1, limit=30, sort_by='created_at', order_by=None, **kwargs):
        """
        Retrieve the scoring information.

        Args:
            board_keys:         <list>
                                board_keys
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

        query_params = {'board_keys': json.dumps(validate_provider_keys(board_keys)),
                        'stage': validate_stage(stage),
                        'limit': validate_limit(limit),
                        'page': validate_page(page),
                        'sort_by': validate_sort_by(sort_by),
                        'order_by': validate_order_by(order_by)
                        }

        params = {**query_params, **kwargs}
        response = self.client.get('jobs/searching', params)
        return response.json()
