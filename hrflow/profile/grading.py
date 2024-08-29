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
        """Init."""
        self.client = api

    @rate_limiter
    def get(
        self,
        algorithm_key: t.Literal[
            "1d07451c0f33091869bd3c6d336dfa4e5c63af74",
            "daaa0f61b72a68b985f31d123ad45b361adc91e4",
        ],
        source_key,
        board_key,
        profile_key=None,
        profile_reference=None,
        job_key=None,
        job_reference=None,
    ):
        """
        💾 Grade a Profile indexed in a Source for a Job
        (https://api.hrflow.ai/v1/profile/grading).

        Args:
            source_key:             <string>
                                    The key of the Source where the profile is indexed.
            key:                    <string>
                                    The Profile unique identifier.
            reference:              <string>
                                    The Profile reference chosen by the customer.
            job_key:                <string>
            job_reference:          <string>
            board_key:              <string>

        Returns
            Get information

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
