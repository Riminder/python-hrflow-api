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


class ProfileStoring:
    """Manage Storing related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    @rate_limiter
    def add_json(self, source_key, profile_json):
        """This endpoint allows you to Index a Profile object.

        Parameters
        ----------
        source_key : string [required]
            Identification key of the Source attached to the Profile.
        profile_json : dict [required]
            A dictionary representing the HrFlow.ai Profile object. The dictionary
            should have the following fields:

            - key (str): Identification key of the Profile.
            - reference (str): Custom identifier of the Profile.
            - text_language (str): Code language of the Profile. Example : `en` for
            English.
            - text (str): Full text of the content of the Profile.
            - consent_algorithmic (dict) : Algorithmic consent status of the Profile.
                - owner (dict) : Owner of the Profile.
                    - parsing (bool)
                    - revealing (bool)
                    - embedding (bool)
                    - searching (bool)
                    - scoring (bool)
                    - upskilling (bool)
            - created_at (str): Creation date of the Profile in ISO 8601 format
            (YYYY-MM-DDTHH:MM:SSZ). This could be the date of the creation of the
            Profile in your ATS.

            ------------------- Profile's info -------------------
            - info (dict): Object containing the Profile's info.
                - full_name (str): Full name of the Profile.
                - first_name (str): First name of the Profile.
                - last_name (str): Last name of the Profile.
                - email (str): Email of the Profile.
                - phone (str): Phone number of the Profile.
                - date_birth (str): Date of birth of the Profile in ISO 8601 format
                (YYYY-MM-DD).
                - location (dict): Main location of the Profile.
                    - text (str): Location text.
                    - lat (float): Latitude coordinate.
                    - lng (float): Longitude coordinate.
                    - fields (dict): Location fields.
                - urls (list): List of urls of the Profile.
                - picture (str): Url of the Profile's picture.
                - gender (str): `male`, `female` or `undefined`.
                - summary (str): Summary of the Profile.
            ------------------- Profile's sections : skills, languages, interests ...
            -------------------
            - skills (list[dict]): List of skills details in the main skills sections
            of a resume or the Profile.
                Each skill is represented by a dictionary with the following fields:
                - name (str): Skill name.
                - type (str): Skill type: `hard` or `soft`.
                - value (any): Skill value. The value attached to the Skill. Example:
                90/100
            - languages (list[dict]): List of languages of the Profile.
                Each language is represented by a dictionary with the following fields:
                - name (str): Language name.
                - value (any): Language value. The value attached to the Language.
                Example: fluent.
            - cetifications (list[dict]): List of certifications of the Profile.
                Each certification is represented by a dictionary with the following
                fields:
                - name (str): Certification name.
                - value (any): Certification value. The value attached to the
                Certification. Example: 4.5/5.
            - courses (list[dict]): List of courses of the Profile.
                Each course is represented by a dictionary with the following fields:
                - name (str): Course name.
                - value (any): Course value. The value attached to the Course.
            - tasks (list[dict]): List of tasks of the Profile.
                Each task is represented by a dictionary with the following fields:
                - name (str): Task name.
                - value (any): Task value. The value attached to the Task.
            - interests (list[dict]): List of interests of the Profile.
                Each interest is represented by a dictionary with the following fields:
                - name (str): Interest name. Example : `music`.
                - value (any): Interest value. The value attached to the Interest.
                Example: beginner.
            ------------------- Profile's experiences and educations
            -------------------
            - experiences_duration (float): Total duration of the Profile's
            experiences in years. Example : 2.5 for 2 years and 6 months.
            - educations_duration (float): Total duration of the Profile's educations
            in years. Example : 2.5 for 2 years and 6 months.
            - experiences (list[dict]): List of the Profile's experiences.
                Each experience is represented by a dictionary with the following
                fields:
                - company (str): Name of the company.
                - title (str): Title of the experience.
                - description (str): Description of the experience.
                - location (dict): Same location object as in the Profile's info.
                - date_start (str): Start date of the experience in ISO 8601 format
                (YYYY-MM-DD).
                - date_end (str): End date of the experience in ISO 8601 format
                (YYYY-MM-DD).
                - skills (list[str]): List of skills used in the experience. Same
                format as the Profile's skills.
                - tasks (list[str]): List of tasks performed in the experience. Same
                format as the Profile's tasks.
                - certifications (list[str]): List of certifications obtained in the
                experience. Same format as the Profile's certifications.
                - courses (list[str]): List of courses followed in the experience.
                Same format as the Profile's courses.
            - educations (list[dict]): List of the Profile's educations.
                Each education is represented by a dictionary with the following
                fields:
                - school (str): Name of the school.
                - title (str): Title of the education.
                - description (str): Description of the education.
                - location (dict): Same location object as in the Profile's info.
                - date_start (str): Start date of the education in ISO 8601 format
                (YYYY-MM-DD).
                - date_end (str): End date of the education in ISO 8601 format
                (YYYY-MM-DD).
                - skills (list[str]): List of skills used in the education. Same
                format as the Profile's skills.
                - tasks (list[str]): List of tasks performed in the education. Same
                format as the Profile's tasks.
                - certifications (list[str]): List of certifications obtained in the
                education. Same format as the Profile's certifications.
                - courses (list[str]): List of courses followed in the education. Same
                format as the Profile's courses.
            ------------------- Profile's attachments, tags and metadatas
            -------------------
            - attachments (list[dict]): List of the Profile's attachments. This field
            currently is internally handeled by HrFlow.ai.
            - tags (list[str]): List of the Profile's tags. Tags are used to extend
            the Profile's information. For example, a tag could be `salary_expectation`.
                Each tag is represented by a dictionary with the following fields:
                - name (str): The name of the Tag. Example: `is_active`.
                - value (any): The value of the Tag. Example: `True`.
            - metadata (list[dict]): Custom metadata added to the Job. They are similar
            to tags, but used for non indexable/searchable information.
                Each metadata is represented by a dictionary with the following fields:
                - name (str): The name of the metadata. Example: `cover_letter`.
                - value (any): The value of the metadata. Example: `I am applying for
                this job because...`.

        Returns
        -------
        dict
            Server response.
        """
        profile_json["source_key"] = validate_key("Source", source_key)
        response = self.client.post("profile/indexing", json=profile_json)
        return validate_response(response)

    @rate_limiter
    def edit(self, source_key, profile_json, key=None):
        """
        Edit a profile already stored in the given source.
        This method uses the endpoint : [PUT] https://api.hrflow.ai/v1/profile/indexing
        It requires :
            - source_key : <string> The key of the source where the profile is stored
            - profile_json : <dict> The profile data to update
                            The profile object must meet the criteria of the HrFlow.ai
                            Profile Object
                            Otherwise the Put request will return an error.
                            A key or a reference must be provided in the profile
                            object `profile_json`, to identify the profile to update.
        The method will update the object already stored by the fields provided in the
        profile_json.
        """
        profile_json["source_key"] = validate_key("Source", source_key)
        # The argument key is kept for backward compatibility with previous versions of
        # the SDK. It should be removed in the future after a Major release
        if key:
            profile_json["key"] = validate_key("Profile", key)

        response = self.client.put("profile/indexing", json=profile_json)
        return validate_response(response)

    @rate_limiter
    def get(self, source_key, key=None, reference=None):
        """
        💾 Get a Profile indexed in a Source
        (https://api.hrflow.ai/v1/profile/indexing).
        Profiles can either be retrieved using this method by their key or their
        reference.
        One of the two values must be provided.

        Args:
            source_key:             <string>
                                    The key of the Source where the profile is indexed.
            key:                    <string>
                                    The Profile unique identifier.
            reference:              <string>
                                    The Profile reference chosen by the customer.

        Returns
            Get information

        """
        query_params = format_item_payload("profile", source_key, key, reference)
        response = self.client.get("profile/indexing", query_params)
        return validate_response(response)

    @rate_limiter
    def archive(self, source_key, key=None, reference=None, email=None):
        """
        This method allows to archive (is_archive=1) or unarchive (is_archive=0) a
        profile in HrFlow.ai.
        The profile is identified by either its key or its reference,
        at least one of the two values must be provided.

        Args:
            source_key:             <string>
                                    source identifier
            key:                    <string>
                                    profile identifier (key)
            reference:              <string>
                                    profile identifier (reference)
            email:                  <string>
                                    profile_email

        Returns
            Archive/unarchive profile response

        """

        payload = format_item_payload("profile", source_key, key, reference, email)
        payload["is_archive"] = 1
        response = self.client.patch("profile/indexing/archive", json=payload)
        return validate_response(response)

    @rate_limiter
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
                                The list of the keys of the Sources containing the
                                targeted Profiles. Example : ["xxx", "yyy", "zzz"]
            name:               <string>
                                The name of the targeted Profiles.
            key:                <string>
                                The key (profile's unique identifier) of the targeted
                                Profiles.
            reference:          <string>
                                The reference of the targeted Profiles.
            location_lat:        <string>
                                The latitude of the targeted Profiles.
            location_lon:        <string>
                                The longitude of the targeted Profiles.
            location_dist:       <string>
                                The distance of the targeted Profiles. (Set a radius
                                around the Profiles'' location address (in Km).)
            return_profile:     <boolean>
                                If set to true, the full JSON of each profile in the
                                array response will be returned, otherwise only the
                                dates, the reference and the keys.
            page:               <integer>
                                The page number of the targeted Profiles.
            limit:              <integer>
                                The number of Profiles to return per page.
            order_by:           <string>
                                The order of the Profiles to return. Possible values
                                are "asc" and "desc".
            sort_by:            <string>
                                The field on which the Profiles will be sorted.
                                Possible values are "created_at" or "updated_at".
            created_at_min:     <string>
                                The minimum date of creation of the targeted Profiles.
                                Format : "YYYY-MM-DD".
            created_at_max:     <string>
                                The maximum date of creation of the targeted Profiles.
                                Format : "YYYY-MM-DD".
        Returns:
            Applies the params to filter on Profiles in the targeted Sources and
            returns the response from the endpoint.
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
