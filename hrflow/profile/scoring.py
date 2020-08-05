import json

from ..utils import validate_key, validate_limit, validate_page, validate_sort_by, validate_order_by, validate_stage, \
    validate_provider_keys


class ProfileScoring():
    """Manage stage related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def get(self, source_keys=None, board_key=None, job_key=None, use_agent=1, agent_key=None,  stage=None, page=1,
            limit=30, sort_by='created_at', order_by=None, **kwargs):
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

        query_params = {'source_keys': json.dumps(validate_provider_keys(source_keys)),
                        'board_key': validate_key('Board', board_key),
                        'job_key': validate_key('Job', job_key),
                        'use_agent': use_agent,
                        'agent_key': validate_key('Agent', agent_key),
                        'stage': validate_stage(stage),
                        'limit': validate_limit(limit),
                        'page': validate_page(page),
                        'sort_by': validate_sort_by(sort_by),
                        'order_by': validate_order_by(order_by)
                        }

        params = {**query_params, **kwargs}
        response = self.client.get('profiles/scoring', params)
        return response.json()
