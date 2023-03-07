import json
from ..utils import (
    validate_boolean,
    validate_key,
    validate_limit,
    validate_page,
    validate_provider_keys,
    validate_response,
    validate_reference,
    ORDER_BY_VALUES,
    SORT_BY_VALUES,
    validate_value,
)


class ProfileStoring:
    """
    This class manages Profiles storing endpoint (https://api.hrflow.ai/v1/storing/profiles).
    This endpoint allows you to retrieve the list of profiles stored in a Source.
    """

    def __init__(self, api):
        """Init."""
        self.client = api

    # Params list
    """
    source_keys:["{{source_key}}"]
    name:
    key:
    reference:
    location_lat:
    location_lon:
    location_dist:
    return_profile:
    page:
    limit:
    order_by:
    sort_by:
    created_at_min:
    created_at_max:
    """

    def list(
        self,
        source_keys,
        name=None,
        key=None,
        reference=None,
        location_lat=None,
        location_lon=None,
        location_dist=None,
        return_profile=False,
        page=1,
        limit=30,
        order_by="desc",
        sort_by="created_at",
        created_at_min=None,
        created_at_max=None,
    ):
        """
        This method allows you to retrieve the list of profiles stored in a Source.

        Args:
            source_keys:        <list>
                                The list of the keys of the Sources containing the targeted Profiles. Example : ["xxx", "yyy", "zzz"]
            name:               <string>
                                The name of the targeted Profiles.
            key:                <string>
                                The key (profile's unique identifier) of the targeted Profiles.
            reference:          <string>
                                The reference of the targeted Profiles.
            location_lat:        <string>
                                The latitude of the targeted Profiles.
            location_lon:        <string>
                                The longitude of the targeted Profiles.
            location_dist:       <string>
                                The distance of the targeted Profiles. (Set a radius around the Profiles'' location address (in Km).)
            return_profile:     <boolean>
                                If set to true, the full JSON of each profile in the array response will be returned, otherwise only the dates, the reference and the keys.
            page:               <integer>
                                The page number of the targeted Profiles.
            limit:              <integer>
                                The number of Profiles to return per page.
            order_by:           <string>
                                The order of the Profiles to return. Possible values are "asc" and "desc".
            sort_by:            <string>
                                The field on which the Profiles will be sorted. Possible values are "created_at" or "updated_at".
            created_at_min:     <string>
                                The minimum date of creation of the targeted Profiles. Format : "YYYY-MM-DD".
            created_at_max:     <string>
                                The maximum date of creation of the targeted Profiles. Format : "YYYY-MM-DD".
        Returns:
            Applies the params to filter on Profiles in the targeted Sources and returns the response from the endpoint.
            Response examples :
                - Success response :
                    {
                        "code": 200, # response code
                        "message": "List of profiles", # response message
                        "meta" : {'page': 1, # current page
                                'maxPage': 5, # max page in the paginated response
                                'count': 2, # number of profiles in the current page
                                'total': 10}, # total number of profiles retrieved
                        "data": [               # list of profiles objects
                            {
                                "key": "xxx",
                                "reference": "xxx",
                                ...
                            },
                            ...
                        ]
                    }
                - Error response : (if the source_key is not valid)
                    {
                        "code": 400,
                        "message": "Invalid parameters. Unable to find object: source"
                    }
        """

        params = {
            "source_keys": json.dumps(validate_provider_keys(source_keys)),
            "name": validate_key("Profile", name),
            "key": validate_key("Profile", key),
            "reference": validate_reference(reference),
            "location_lat": location_lat,  # TODO : validate_location_lat(location_lat),
            "location_lon": location_lon,  # TODO : validate_location_lon(location_lon),
            "location_dist": location_dist,
            "return_profile": validate_boolean("return_profile", return_profile),
            "page": validate_page(page),
            "limit": validate_limit(limit),
            "order_by": validate_value(order_by, ORDER_BY_VALUES, "order by"),
            "sort_by": validate_value(sort_by, SORT_BY_VALUES, "sort by"),
            "created_at_min": created_at_min,  # TODO validate dates format
            "created_at_max": created_at_max,  # TODO validate dates format
        }
        response = self.client.get("storing/profiles", params)
        return validate_response(response)
