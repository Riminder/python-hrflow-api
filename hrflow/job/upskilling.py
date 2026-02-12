import typing as t

from ..core.rate_limit import rate_limiter
from ..core.validation import (
    KEY_REGEX,
    validate_key,
    validate_reference,
    validate_response,
    validate_score,
)


class JobUpskilling:
    def __init__(self, api):
        """Initialize the JobUpskilling class with the provided API client."""
        self.client = api

    @rate_limiter
    def get(
        self,
        board_key: str,
        source_key: str,
        score: float,
        job_key: t.Optional[str] = None,
        job_reference: t.Optional[str] = None,
        profile_key: t.Optional[str] = None,
        profile_reference: t.Optional[str] = None,
    ) -> t.Dict[str, t.Any]:
        """
        Explain a Job recommendation for a Profile
        (https://api.hrflow.ai/v1/job/upskilling).

        Args:
            board_key:              <string>
                                    The key of the Board where the job is indexed.
            source_key:             <string>
                                    The key of the Source where the profile is indexed.
            score:                  <float>
                                    The recommendation score. Must be between 0 and 1
                                    (exclusive).
            job_key:                <string>
                                    (Optional) The Job unique identifier.
            job_reference:          <string>
                                    (Optional) The Job reference chosen by the customer.
            profile_key:            <string>
                                    (Optional) The Profile unique identifier.
            profile_reference:      <string>
                                    (Optional) The Profile reference chosen by the customer.

        Returns:
            Explanation of why the job is recommended for the profile.
        """
        query_params = {
            "board_key": validate_key("Board", board_key, regex=KEY_REGEX),
            "source_key": validate_key("Source", source_key, regex=KEY_REGEX),
            "score": validate_score(score),
            "job_key": validate_key("Key", job_key, regex=KEY_REGEX),
            "job_reference": validate_reference(job_reference),
            "profile_key": validate_key("Key", profile_key, regex=KEY_REGEX),
            "profile_reference": validate_reference(profile_reference),
        }

        response = self.client.get("job/upskilling", query_params)
        return validate_response(response)
