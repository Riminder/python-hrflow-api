import json
import time
from .validator import validate_source_ids, validate_stage, validate_timestamp, validate_limit, validate_page, \
    validate_sort_by, validate_order_by

TIMESTAMP_NOW = time.time()


class ProfileSearching():
    """Manage stage related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def get(self, source_ids=None, stage=None, date_start="1494539999", date_end=TIMESTAMP_NOW,
               page=1, limit=30, sort_by='date_reception', order_by=None, **kwargs):
        """
        Retreive all profiles that match the query param.

        Args:
            date_end:   <string> REQUIRED (default to timestamp of now)
                        profiles' last date of reception
            date_start: <string> REQUIRED (default to "1494539999")
                        profiles' first date of reception
            limit:      <int> (default to 30)
                        number of fetched profiles/page
            page:       <int> REQUIRED default to 1
                        number of the page associated to the pagination
            sort_by:    <string>
            source_ids: <array of strings> REQUIRED
            stage:      <string>

        Returns
            Retrieve the profiles data as <dict>

        """
        query_params = {"source_ids": json.dumps(validate_source_ids(source_ids)),
                        "stage": validate_stage(stage),
                        "date_end": validate_timestamp(date_end, "date_end"),
                        "date_start": validate_timestamp(date_start, "date_start"),
                        "limit": validate_limit(limit),
                        "page": validate_page(page),
                        "sort_by": validate_sort_by(sort_by),
                        "order_by": validate_order_by(order_by)
                        }

        params = {**query_params, **kwargs}
        response = self.client.get("profiles/searching", params)
        return response.json()
