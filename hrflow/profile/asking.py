import typing as t

from ..core.rate_limit import rate_limiter
from ..core.validation import (
    KEY_REGEX,
    validate_key,
    validate_reference,
    validate_response,
)


class ProfileAsking:
    def __init__(self, api):
        self.client = api

    @rate_limiter
    def get(
        self,
        source_key: str,
        questions: t.List[str],
        reference: t.Optional[str] = None,
        key: t.Optional[str] = None,
    ) -> t.Dict[str, t.Any]:
        """
        Ask a question to a Profile indexed in a Source. This endpoint allows asking a
        question based on a Profile object.

        Args:
            source_key:     <str>
                            The key of the Source associated to the profile.
            questions:      <list[str]>
                            Question based on the queried profile.
            reference:      str
                            The Profile reference chosen by the customer.
            key:            str
                            The Profile unique identifier

        Returns:
            `/profile/asking` response
        """

        params = dict(
            source_key=validate_key("Source", source_key, regex=KEY_REGEX),
            reference=validate_reference(reference),
            key=validate_key("Profile", key, regex=KEY_REGEX),
            questions=questions,
        )

        response = self.client.get("profile/asking", query_params=params)

        return validate_response(response)
