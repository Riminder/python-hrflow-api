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
        """Initialize the ProfileMatching class with the provided API client."""
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
        💾 Match Profils indexed in Sources to a Profile
        (https://api.hrflow.ai/v1/profils/matching).

        Args:
            source_key:         <string>
                                The key of the Source in which the profile is indexed.
            profile_key:        <string> (Optional)
                                The key of a specific profile to macth with.
            profile_reference:  <string> (Optional)
                                The reference of a specific profile to macth with.
            source_keys:        <list> (Optional)
                                A list of keys for multiple Sources of profiles to be matched with the profile.
            page:               <int> (default to 1)
                                The page number for pagination.
            limit:              <int> (default to 30)
                                Number of profiles to fetch per page.
            sort_by:            <string> (default to "created_at")
                                The field to sort by.
            order_by:           <string> (Optional)
                                The order of sorting, either 'asc' or 'desc'.
            created_at_min:     <string> (Optional)
                                The minimum creation date of the profiles in format "YYYY-MM-DD".
            created_at_max:     <string> (Optional)
                                The maximum creation date of the profiles in format "YYYY-MM-DD".

        Returns:
            Match the profile identified by profile_key or profile_reference
            and source_key with all profiles in the sources identified by keys in source_keys list.

            Response examples:
                - Success response:
                    {
                        "code": 200, # response code
                        "message": "Profile Matching results", # response message
                        "meta": {
                            'page': 1, # current page
                            'maxPage': 5, # max page in the paginated response
                            'count': 2, # number of profiles in the current page
                            'total': 10 # total number of profiles retrieved
                        },
                        "data": {  # list of profile objects
                            "predictions": [[]],
                            "profiles": [
                                {
                                    "key": "xxx",
                                    "reference": "xxx",
                                    ...
                                },
                                ...
                            ]
                        }
                    }
                - Error response: (if the source_key is not valid)
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
