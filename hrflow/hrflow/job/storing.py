import json
from ..utils import (
    format_item_payload,
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
    """Manage Storing related job calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def add_json(self, board_key, job_json):
        """Use the api to add a new profile using profile_data."""
        job_json["board_key"] = validate_key("Board", board_key)
        response = self.client.post("job/indexing", json=job_json)
        return validate_response(response)

    def edit(self, board_key, job_json, key=None):
        """
        Edit a job already stored in the given source.
        This method uses the endpoint : [PUT] https://api.hrflow.ai/v1/job/indexing
        It requires : 
            - source_key : <string> The key of the source where the job is stored
            - job_json : <dict> The job data to update
                            The job object must meet the criteria of the HrFlow.ai job Object
                            Otherwise the Put request will return an error. 
                            A key or a reference must be provided in the job object `job_json`, to identify the job to update.
        The method will update the object already stored by the fields provided in the job_json.
        """

        if job_json is None:
            job_json = {}

        job_json["board_key"] = validate_key("Board", board_key)
        # The argument key is kept for backward compatibility with previous versions of the SDK
        # It should be removed in the future after a Major release
        if key:
            job_json["key"] = validate_key("Job", key)
            
        response = self.client.put("job/indexing", json=job_json)
        return validate_response(response)

    def get(self, board_key, key=None, reference=None):
        """
        Retrieve the parsing information.

        Args:
            board_key:              <string>
                                    board id
            key:                    <string>
                                    job id
            reference:              <string>
                                    job_reference

        Returns
            parsing information

        """
        query_params = format_item_payload("job", board_key, key, reference)
        response = self.client.get("job/indexing", query_params)
        return validate_response(response)

    def archive(self, board_key, key=None, reference=None, is_archive=1):
        """
        This method allows to archive (is_archive=1) or unarchive (is_archive=0) a job
        in HrFlow.ai.
        The job is identified by either its key or its reference,
        at least one of the two values must be provided.

        Args:
            board_key:             <string>
                                    board identifier
            key:                    <string>
                                    job identifier (key)
            reference:              <string>
                                    job identifier (reference)
            is_archive:             <integer>
                                    default = 1
                                    {0, 1} to indicate archive/unarchive action

        Returns
            Archive/unarchive job response

        """
        payload = format_item_payload("job", board_key, key, reference)
        payload["is_archive"] = is_archive
        response = self.client.patch("job/indexing/archive", json=payload)
        return validate_response(response)

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
