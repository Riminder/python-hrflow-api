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


class JobStoring:
    """
    This class manages Jobs Storing endpoint (https://api.hrflow.ai/v1/storing/jobs).
    This endpoint allows you to retrieve the list of jobs stored in a Board.
    """

    def __init__(self, api):
        """Init."""
        self.client = api

    def list(
        self,
        board_keys,
        name=None,
        key=None,
        reference=None,
        location_lat=None,
        location_lon=None,
        location_dist=None,
        return_job=False,
        page=1,
        limit=30,
        order_by="desc",
        sort_by="created_at",
        created_at_min=None,
        created_at_max=None,
    ):
        """
        This method allows you to retrieve the list of jobs stored in a Board.

        Args:
            board_keys:         <list>
                                The list of the keys of the Boards containing the targeted Jobs. Example : ["xxx", "yyy", "zzz"]
            name:               <string>
                                The name of the targeted Jobs.
            key:                <string>
                                The key (job's unique identifier) of the targeted Jobs.
            reference:          <string>
                                The reference of the targeted Jobs.
            location_lat:        <string>
                                The latitude of the targeted Jobs.
            location_lon:        <string>
                                The longitude of the targeted Jobs.
            location_dist:       <string>
                                The distance of the targeted Jobs. (Set a radius around the Jobs'' location address (in Km).)
            return_job:         <boolean>
                                If set to true, the full JSON of each job in the array response will be returned, otherwise only the dates, the reference and the keys.
            page:               <integer>
                                The page number of the targeted Jobs.
            limit:              <integer>
                                The number of Jobs to return per page.
            order_by:           <string>
                                The order of the Jobs to return. Possible values are "asc" and "desc".
            sort_by:            <string>
                                The field on which the Jobs will be sorted. Possible values are "created_at" or "updated_at".
            created_at_min:     <string>
                                The minimum date of creation of the targeted Jobs. Format : "YYYY-MM-DD".
            created_at_max:     <string>
                                The maximum date of creation of the targeted Jobs. Format : "YYYY-MM-DD".
        Returns:
            Applies the params to filter on Jobs in the targeted Boards and returns the response from the endpoint.
            Response examples :
                - Success response :
                    {
                        "code": 200, # response code
                        "message": "List of jobs", # response message
                        "meta" : {'page': 1, # current page
                                'maxPage': 5, # max page in the paginated response
                                'count': 2, # number of jobs in the current page
                                'total': 10}, # total number of jobs retrieved
                        "data": [               # list of jobs objects
                            {
                                "key": "xxx",
                                "reference": "xxx",
                                ...
                            },
                            ...
                        ]
                    }
                - Error response :
                    {
                        "code": 400,
                        "message": "Invalid parameters. Unable to find object: board"
                    }
        """

        params = {
            "board_keys": json.dumps(validate_provider_keys(board_keys)),
            "name": validate_key("Job", name),
            "key": validate_key("Job", key),
            "reference": validate_reference(reference),
            "location_lat": location_lat,  # TODO : validate_location_lat(location_lat),
            "location_lon": location_lon,  # TODO : validate_location_lon(location_lon),
            "location_dist": location_dist,
            "return_job": validate_boolean("return_job", return_job),
            "page": validate_page(page),
            "limit": validate_limit(limit),
            "order_by": validate_value(order_by, ORDER_BY_VALUES, "order by"),
            "sort_by": validate_value(sort_by, SORT_BY_VALUES, "sort by"),
            "created_at_min": created_at_min,  # TODO validate dates format
            "created_at_max": created_at_max,  # TODO validate dates format
        }

        response = self.client.get("storing/jobs", params)
        return validate_response(response)


"""
{'code': 400, 'message': 'Invalid parameters. Unable to find object: source'}
"""
