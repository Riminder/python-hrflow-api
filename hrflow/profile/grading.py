import json
import typing as t

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


class ProfileGrading:
    def __init__(self, api):
        """Initialize the ProfileGrading class with the provided API client."""
        self.client = api

    @rate_limiter
    def get(
        self,
        algorithm_key: str,
        source_key: str,
        board_key: str,
        profile_key: t.Optional[str] = None,
        profile_reference: t.Optional[str] = None,
        job_key: t.Optional[str] = None,
        job_reference: t.Optional[str] = None,
    ):
        """
        💾 Grade a Profile indexed in a Source for a Job
        (https://api.hrflow.ai/v1/profile/grading).

        Args:
            algorithm_key:          <string>
                                    The key of the grading algorithm to use.
                                    Refer to the documentation: https://developers.hrflow.ai/reference/grade-a-profile-indexed-in-a-source-for-a-job
                                    for all possible values.
            source_key:             <string>
                                    The key of the Source where the profile to grade is indexed.
            board_key:              <string>
                                    The key of the Board where the job to grade to is indexed.
            profile_key:            <string>
                                    (Optional) The Profile unique identifier.
            profile_reference:      <string>
                                    (Optional) The Profile reference chosen by the customer.
            job_key:                <string>
                                    (Optional) The Job unique identifier.
            job_reference:          <string>
                                    (Optional) The Job reference chosen by the customer.

        Returns:
            The grading information for the profile, based on the specified job.

        """
        query_params = {
            "algorithm_key": algorithm_key,
            "source_key": validate_key("Source", source_key, regex=KEY_REGEX),
            "profile_key": validate_key("Key", profile_key, regex=KEY_REGEX),
            "profile_reference": validate_reference(profile_reference),
            "board_key": validate_key("Board", board_key, regex=KEY_REGEX),
            "job_key": validate_key("Key", job_key, regex=KEY_REGEX),
            "job_reference": validate_reference(job_reference),
        }

        response = self.client.get("profile/grading", query_params)
        return validate_response(response)
