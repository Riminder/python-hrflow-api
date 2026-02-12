import typing as t

from ..core.rate_limit import rate_limiter
from ..core.validation import (
    KEY_REGEX,
    validate_key,
    validate_reference,
    validate_response,
)


class JobGrading:
    def __init__(self, api):
        """Initialize the JobGrading class with the provided API client."""
        self.client = api

    @rate_limiter
    def get(
        self,
        algorithm_key: str,
        board_key: str,
        source_key: str,
        job_key: t.Optional[str] = None,
        job_reference: t.Optional[str] = None,
        profile_key: t.Optional[str] = None,
        profile_reference: t.Optional[str] = None,
    ):
        """
        Grade Jobs indexed in a Board for a Profile
        (https://api.hrflow.ai/v1/job/grading).

        Args:
            algorithm_key:          <string>
                                    The key of the grading algorithm to use.
            board_key:              <string>
                                    The key of the Board where the job is indexed.
            source_key:             <string>
                                    The key of the Source where the profile is indexed.
            job_key:                <string>
                                    (Optional) The Job unique identifier.
            job_reference:          <string>
                                    (Optional) The Job reference chosen by the customer.
            profile_key:            <string>
                                    (Optional) The Profile unique identifier.
            profile_reference:      <string>
                                    (Optional) The Profile reference chosen by the customer.

        Returns:
            The grading information for the job, based on the specified profile.
        """
        query_params = {
            "algorithm_key": algorithm_key,
            "board_key": validate_key("Board", board_key, regex=KEY_REGEX),
            "job_key": validate_key("Key", job_key, regex=KEY_REGEX),
            "job_reference": validate_reference(job_reference),
            "source_key": validate_key("Source", source_key, regex=KEY_REGEX),
            "profile_key": validate_key("Key", profile_key, regex=KEY_REGEX),
            "profile_reference": validate_reference(profile_reference),
        }

        response = self.client.get("job/grading", query_params)
        return validate_response(response)
