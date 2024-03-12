import json

from ..core import format_item_payload
from ..core.rate_limit import rate_limiter
from ..core.validation import (
    ORDER_BY_VALUES,
    SORT_BY_VALUES,
    validate_boolean,
    validate_key,
    validate_limit,
    validate_page,
    validate_provider_keys,
    validate_reference,
    validate_response,
    validate_value,
)


class JobStoring:
    """Manage Storing related job calls."""

    def __init__(self, api):
        """_summary_

        Parameters
        ----------
        api : _type_
            _description_
        """
        self.client = api

    @rate_limiter
    def add_json(self, board_key, job_json):
        """This endpoint allows you to Index a Job object.
        Note: If your Job is an unstructured text, make sure to parse it first before
        indexing it.
            See how in 🧠 Parse a raw Text at: https://developers.hrflow.ai/ .
        Parameters
        ----------
        board_key : string [required]
            Identification key of the Board attached to the Job.
        job_json : dict [required]
            A dictionary representing the HrFlow.ai Job object. The dictionary should
            have the following fields:

            - key (str): Identification key of the Job.
            - reference (str): Custom identifier of the Job.
            - name (str) [required]: Job title.
            - location (dict): Location information for the job.
                - text (str): Location text.
                - lat (float): Latitude coordinate.
                - lng (float): Longitude coordinate.
            - sections (list[dict]): List of sections in the job.
                Each section is represented by a dictionary with the following fields:
                - name (str): Section name.
                - title (str): Section title.
                - description (str): Section description.
            - url (str): Job post original URL.
            - summary (str): Brief summary of the Job.
            - created_at (str): Creation date of the Job in ISO 8601 format
            (YYYY-MM-DDTHH:MM:SSZ).
            - skills (list[dict]): List of skills required for the Job.
                Each skill is represented by a dictionary with the following fields:
                - name (str): Skill name.
                - type (str): Skill type: `hard` or `soft`.
                - value (any): Skill value. The value attached to the Skill.
                Example: 90/100
            - languages (list[dict]): List of languages required for the Job.
                Each language is represented by a dictionary with the following fields:
                - name (str): Language name.
                - value (any): Language value. The value attached to the Language.
                Example: fluent.
            - cetifications (list[dict]): List of certifications required for the Job.
                Each certification is represented by a dictionary with the following
                fields:
                - name (str): Certification name.
                - value (any): Certification value. The value attached to the
                Certification. Example: 4.5/5.
            - courses (list[dict]): List of courses required for the Job.
                Each course is represented by a dictionary with the following fields:
                - name (str): Course name.
                - value (any): Course value. The value attached to the Course.
            - tasks (list[dict]): List of tasks required for the Job.
                Each task is represented by a dictionary with the following fields:
                - name (str): Task name.
                - value (any): Task value. The value attached to the Task.
            - tags (list[dict]): List of tags added to the Job. Tags are a way we can
            extend the Job object with custom information.
                Each tag is represented by a dictionary with the following fields:
                - name (str): The name of the Tag. Example: `is_active`.
                - value (any): The value of the Tag. Example: `True`.
            - metadata (list[dict]): Custom metadata added to the Job.
                Each metadata is represented by a dictionary with the following fields:
                - name (str): The name of the metadata. Example: interview-note
                - value (any): The value of the metadata. Example: `The candidate was
                very good ...`.
            - ranges_float (list[dict]): List of float ranges added to the Job.
                Each range is represented by a dictionary with the following fields:
                - name (str): The name of the range. Example: salary.
                - value_min (float): The minimum value of the range. Example: 50000.
                - value_max (float): The maximum value of the range. Example: 60000.
                - unit (str): The unit of the range. Example: EUR.
            - ranges_date (list[dict]): List of date ranges added to the Job.
                Each range is represented by a dictionary with the following fields:
                - name (str): The name of the range. Example: availability.
                - value_min (str): The minimum value of the range in ISO 8601 format
                (YYYY-MM-DDTHH:MM:SSZ). Example: 2020-01-01.
                - value_max (str): The maximum value of the range in ISO 8601 format
                (YYYY-MM-DDTHH:MM:SSZ). Example: 2020-03-01.
            - culture (str): The company culture description in the Job.
            - benefits (str): The job opening benefits description in the Job.
            - responsibilities (str): The job opening responsibilities description in
            the Job.
            - requirements (str): The job opening requirements description in the Job.
            - interviews (str): The job opening interviews.
        Returns
        -------
        dict
            Server response.
        """
        job_json["board_key"] = validate_key("Board", board_key)
        response = self.client.post("job/indexing", json=job_json)
        return validate_response(response)

    @rate_limiter
    def edit(self, board_key, job_json, key=None):
        """
        Edit a job already stored in the given source.
        This method uses the endpoint : [PUT] https://api.hrflow.ai/v1/job/indexing
        It requires :
            - source_key : <string> The key of the source where the job is stored
            - job_json : <dict> The job data to update
                            The job object must meet the criteria of the HrFlow.ai
                            job Object
                            Otherwise the Put request will return an error.
                            A key or a reference must be provided in the job object
                            `job_json`, to identify the job to update.
        The method will update the object already stored by the fields provided in
        the job_json.
        """

        if job_json is None:
            job_json = {}

        job_json["board_key"] = validate_key("Board", board_key)
        # The argument key is kept for backward compatibility with previous versions
        # of the SDK. It should be removed in the future after a Major release.
        if key:
            job_json["key"] = validate_key("Job", key)

        response = self.client.put("job/indexing", json=job_json)
        return validate_response(response)

    @rate_limiter
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

    @rate_limiter
    def archive(self, board_key, key=None, reference=None):
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

        Returns
            Archive/unarchive job response

        """
        payload = format_item_payload("job", board_key, key, reference)
        payload["is_archive"] = 1
        response = self.client.patch("job/indexing/archive", json=payload)
        return validate_response(response)

    @rate_limiter
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
                                The list of the keys of the Boards containing the
                                targeted Jobs. Example : ["xxx", "yyy", "zzz"]
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
                                The distance of the targeted Jobs. (Set a radius
                                around the Jobs'' location address (in Km).)
            return_job:         <boolean>
                                If set to true, the full JSON of each job in the
                                array response will be returned, otherwise only the
                                dates, the reference and the keys.
            page:               <integer>
                                The page number of the targeted Jobs.
            limit:              <integer>
                                The number of Jobs to return per page.
            order_by:           <string>
                                The order of the Jobs to return. Possible values are
                                "asc" and "desc".
            sort_by:            <string>
                                The field on which the Jobs will be sorted. Possible
                                values are "created_at" or "updated_at".
            created_at_min:     <string>
                                The minimum date of creation of the targeted Jobs.
                                Format : "YYYY-MM-DD".
            created_at_max:     <string>
                                The maximum date of creation of the targeted Jobs.
                                Format : "YYYY-MM-DD".
        Returns:
            Applies the params to filter on Jobs in the targeted Boards and returns
            the response from the endpoint.
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
