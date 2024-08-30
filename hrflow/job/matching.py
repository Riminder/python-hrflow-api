import json

from ..core.rate_limit import rate_limiter
from ..core.validation import (
    KEY_REGEX,
    ORDER_BY_VALUES,
    SORT_BY_VALUES,
    validate_key,
    validate_limit,
    validate_page,
    validate_provider_keys,
    validate_reference,
    validate_response,
    validate_value,
)


class JobMatching:
    def __init__(self, api):
        """Init."""
        self.client = api

    @rate_limiter
    def list(
        self,
        board_key,
        job_key=None,
        job_reference=None,
        board_keys=None,
        page=1,
        limit=30,
        sort_by="created_at",
        order_by=None,
        created_at_min=None,
        created_at_max=None,
        **kwargs,
    ):
        """
        💾 Match Jobs indexed in Boards to a Job
        (https://api.hrflow.ai/v1/jobs/matching).

        Args:
            board_key:         <string>
                               The key of the Board in which the job is indexed.
            job_key:           <string>
                               The key of a specific job to macth with.
            job_reference:     <string>
                               The reference of a specific job to macth with.
            board_keys:        <list>
                               A list of keys for multiple Boards of profiles to be matched with the specific job.
                               Example : ["xxx", "yyy", "zzz"]
            limit:             <int> (default to 30)
                               number of fetched jobs/page
            page:              <int> REQUIRED default to 1
                               number of the page associated to the pagination
            sort_by:           <string>
            order_by:          <string>
            created_at_min:    <string>
                               The minimum date of creation of the targeted Jobs.
                               Format: "YYYY-MM-DD".
            created_at_max:    <string>
                               The maximum date of creation of the targeted Jobs.
                               Format: "YYYY-MM-DD".

        Returns:
            Match the job identified by job_key or job_reference
            and board_key with all jobs in the boards identified by keys in board_keys list.
            Response examples:
                - Success response:
                    {
                        "code": 200, # response code
                        "message": "Job Matching results", # response message
                        "meta" : {
                            'page': 1, # current page
                            'maxPage': 5, # max page in the paginated response
                            'count': 2, # number of jobs in the current page
                            'total': 10 # total number of jobs retrieved
                        },
                        "data": {  # list of jobs objects
                            "predictions": [[]],
                            "jobs": [
                                {
                                    "key": "xxx",
                                    "reference": "xxx",
                                    ...
                                },
                                ...
                            ]
                        }
                    }
                - Error response: (if the board_key is not valid)
                    {
                        "code": 400,
                        "message": "Invalid parameters. Unable to find object: source"
                    }
        """

        query_params = {
            "board_key": validate_key("Board", board_key, regex=KEY_REGEX),
            "job_key": validate_key("Key", job_key, regex=KEY_REGEX),
            "job_reference": validate_reference(job_reference),
            "board_keys": json.dumps(validate_provider_keys(board_keys)),
            "limit": validate_limit(limit),
            "page": validate_page(page),
            "sort_by": validate_value(sort_by, SORT_BY_VALUES, "sort by"),
            "order_by": validate_value(order_by, ORDER_BY_VALUES, "order by"),
            "created_at_min": created_at_min,  # TODO validate dates format
            "created_at_max": created_at_max,  # TODO validate dates format
        }

        params = {**query_params, **kwargs}
        response = self.client.get("jobs/matching", params)
        return validate_response(response)
