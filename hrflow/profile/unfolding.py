import typing as t

from ..core.rate_limit import rate_limiter
from ..core.validation import (
    KEY_REGEX,
    validate_key,
    validate_reference,
    validate_response,
)


class ProfileUnfolding:
    def __init__(self, api):
        self.client = api

    @rate_limiter
    def get(
        self,
        source_key: str,
        reference: t.Optional[str] = None,
        key: t.Optional[str] = None,
        max_steps: int = 1,
        job_text: t.Optional[str] = None,
    ) -> t.Dict[str, t.Any]:
        """
        Unfold the career path of a Profile. This endpoint allows predicting the
        future experiences and educations of a profile.

        Args:
            source_key:     <str>
                            The key of the Source associated to the profile.
            key:            <Optional[str]>
                            The Profile unique identifier.
            reference:      <Optional[str]>
                            The Profile reference chosen by the customer.
            max_steps:      <int>
                            Number of predicted experiences to get into the target
                            job position.
            job_text:       <Optional[str]>
                            Target job description

        Returns:
            `/profile/unholding` response
        """

        params = dict(
            source_key=validate_key("Source", source_key, regex=KEY_REGEX),
            reference=validate_reference(reference),
            key=validate_key("Key", key, regex=KEY_REGEX),
            max_steps=max_steps,
            job_text=job_text,
        )

        response = self.client.get("profile/unfolding", query_params=params)

        return validate_response(response)
