import json
import time
from .validator import validate_source_ids, validate_job_id, validate_stage, validate_timestamp, validate_limit, validate_page, \
    validate_sort_by, validate_order_by

TIMESTAMP_NOW = time.time()


class ProfileScoring():
    """Manage stage related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def get(self, source_ids=None, job_id=None, stage=None, use_agent=None, date_start="1494539999", date_end=TIMESTAMP_NOW,
            page=1, limit=30, sort_by='date_reception', order_by=None, **kwargs):
        """
        Retrieve the scoring information.

        Args:
            source_ids:         <list>
                                source ids
            job_id:             <string>
                                job id
            stage:              <string>
                                stage
            use_agent:          <int>
                                use_agent
            date_end:           <string> REQUIRED (default to timestamp of now)
                                profiles' last date of reception
            date_start:         <string> REQUIRED (default to "1494539999")
                                profiles' first date of reception
            limit:              <int> (default to 30)
                                number of fetched profiles/page
            page:               <int> REQUIRED default to 1
                                number of the page associated to the pagination
            sort_by:            <string>
            order_by:           <string>

        Returns
            parsing information

        """
        query_params = {}

        query_params = {"source_ids": json.dumps(validate_source_ids(source_ids)),
                        "stage": validate_stage(stage),
                        "date_end": validate_timestamp(date_end, "date_end"),
                        "date_start": validate_timestamp(date_start, "date_start"),
                        "limit": validate_limit(limit),
                        "page": validate_page(page),
                        "sort_by": validate_sort_by(sort_by),
                        "order_by": validate_order_by(order_by),
                        "use_agent": use_agent
                        }
        if job_id:
            query_params["job_id"] = validate_job_id(job_id)

        params = {**query_params, **kwargs}
        response = self.client.get('profiles/scoring', params)
        return response.json()
