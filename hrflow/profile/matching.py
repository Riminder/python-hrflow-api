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


class ProfileMatching:
    def __init__(self, api):
        """Init."""
        self.client = api

    @rate_limiter
    def list(
        self,
        source_key,
        profile_key=None,
        profile_reference=None,
        source_keys=None,
        page=1,
        limit=30,
        sort_by="created_at",
        order_by=None,
        created_at_min=None,
        created_at_max=None,
        **kwargs,
    ):
        """
        Retrieve the matching information.

        Args:
            profile_key:        <string>
            profile_reference:  <string>
            source_key:         <string>
            source_keys:        <list>
                                source_keys
            limit:              <int> (default to 30)
                                number of fetched profiles/page
            page:               <int> REQUIRED default to 1
                                number of the page associated to the pagination
            sort_by:            <string>
            order_by:           <string>
            created_at_min:     <string>
                                The minimum date of creation of the targeted Profiles.
                                Format : "YYYY-MM-DD".
            created_at_max:     <string>
                                The maximum date of creation of the targeted Profiles.
                                Format : "YYYY-MM-DD".
        Returns
            Applies the params to filter on Profiles in the targeted Sources and
            returns the response from the endpoint.
            Response examples :
                - Success response :
                    {
                        "code": 200, # response code
                        "message": "Profile Matching results", # response message
                        "meta" : {'page': 1, # current page
                                'maxPage': 5, # max page in the paginated response
                                'count': 2, # number of profiles in the current page
                                'total': 10}, # total number of profiles retrieved
                        "data": {               # list of profiles objects
                            "predictions":[
                                []
                            ]
                            "profiles":[
                            {
                                "key": "xxx",
                                "reference": "xxx",
                                ...
                            },
                            ...
                            ]
                        }
                    }
                - Error response : (if the source_key is not valid)
                    {
                        "code": 400,
                        "message": "Invalid parameters. Unable to find object: source"
                    }

        """

        query_params = {
            "source_key": validate_key("Source", source_key, regex=KEY_REGEX),
            "profile_key": validate_key("Key", profile_key, regex=KEY_REGEX),
            "profile_reference": validate_reference(profile_reference),
            "source_keys": json.dumps(validate_provider_keys(source_keys)),
            "limit": validate_limit(limit),
            "page": validate_page(page),
            "sort_by": validate_value(sort_by, SORT_BY_VALUES, "sort by"),
            "order_by": validate_value(order_by, ORDER_BY_VALUES, "order by"),
            "created_at_min": created_at_min,  # TODO validate dates format
            "created_at_max": created_at_max,  # TODO validate dates format
        }

        params = {**query_params, **kwargs}
        response = self.client.get("profiles/matching", params)
        return validate_response(response)
