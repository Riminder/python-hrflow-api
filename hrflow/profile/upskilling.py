import typing as t

from ..core.rate_limit import rate_limiter
from ..core.validation import (
    KEY_REGEX,
    validate_key,
    validate_reference,
    validate_response,
)


class ProfileUpskilling:
    def __init__(self, api):
        """Initialize the ProfileUpskilling class with the provided API client."""
        self.client = api

    @rate_limiter
    def get(
        self,
        source_key: str,
        board_key: str,
        profile_key: t.Optional[str] = None,
        profile_reference: t.Optional[str] = None,
        job_key: t.Optional[str] = None,
        job_reference: t.Optional[str] = None,
    ) -> t.Dict[str, t.Any]:
        """
        Explain a Profile recommendation for a Job
        (https://api.hrflow.ai/v1/profile/upskilling).

        Args:
            source_key:             <string>
                                    The key of the Source where the profile is indexed.
            board_key:              <string>
                                    The key of the Board where the job is indexed.
            profile_key:            <string>
                                    (Optional) The Profile unique identifier.
            profile_reference:      <string>
                                    (Optional) The Profile reference chosen by the customer.
            job_key:                <string>
                                    (Optional) The Job unique identifier.
            job_reference:          <string>
                                    (Optional) The Job reference chosen by the customer.

        Returns:
            Explanation of why the profile is recommended for the job.
        """
        query_params = {
            "source_key": validate_key("Source", source_key, regex=KEY_REGEX),
            "board_key": validate_key("Board", board_key, regex=KEY_REGEX),
            "profile_key": validate_key("Key", profile_key, regex=KEY_REGEX),
            "profile_reference": validate_reference(profile_reference),
            "job_key": validate_key("Key", job_key, regex=KEY_REGEX),
            "job_reference": validate_reference(job_reference),
        }

        response = self.client.get("profile/upskilling", query_params)
        return validate_response(response)
