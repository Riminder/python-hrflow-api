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


class ProfileStoring:
    """Manage Storing related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def add_json(self, source_key, profile_json):
        """Use the api to add a new profile using profile_data."""
        profile_json["source_key"] = validate_key("Source", source_key)
        response = self.client.post("profile/indexing", json=profile_json)
        return validate_response(response)

    def edit(self, source_key, profile_json, key=None):
        """
        Edit a profile already stored in the given source.
        This method uses the endpoint : [PUT] https://api.hrflow.ai/v1/profile/indexing
        It requires : 
            - source_key : <string> The key of the source where the profile is stored
            - profile_json : <dict> The profile data to update
                            The profile object must meet the criteria of the HrFlow.ai Profile Object
                            Otherwise the Put request will return an error. 
                            A key or a reference must be provided in the profile object `profile_json`, to identify the profile to update.
        The method will update the object already stored by the fields provided in the profile_json.
        """
        profile_json["source_key"] = validate_key("Source", source_key)
        # The argument key is kept for backward compatibility with previous versions of the SDK
        # It should be removed in the future after a Major release
        if key:
            profile_json["key"] = validate_key("Profile", key)
            
        response = self.client.put("profile/indexing", json=profile_json)
        return validate_response(response)

    def get(self, source_key, key=None, reference=None):
        """
        💾 Get a Profile indexed in a Source (https://api.hrflow.ai/v1/profile/indexing).
        Profiles can either be retrieved using this method by their key or their reference.
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

    def archive(self, source_key, key=None, reference=None, is_archive=1, email=None):
        """
        This method allows to archive (is_archive=1) or unarchive (is_archive=0)a profile
        in HrFlow.ai.
        The profile is identified by either its key or its reference,
        at least one of the two values must be provided.

        Args:
            source_key:             <string>
                                    source identifier
            key:                    <string>
                                    profile identifier (key)
            reference:              <string>
                                    profile identifier (reference)
            is_archive:             <integer>
                                    default = 1
                                    {0, 1} to indicate archive/unarchive action
            email:                  <string>
                                    profile_email

        Returns
            Archive/unarchive profile response

        """

        payload = format_item_payload("profile", source_key, key, reference, email)
        payload["is_archive"] = is_archive
        response = self.client.patch("profile/indexing/archive", json=payload)
        return validate_response(response)

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
