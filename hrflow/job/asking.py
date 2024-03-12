import typing as t

from ..core.rate_limit import rate_limiter
from ..core.validation import (
    KEY_REGEX,
    validate_key,
    validate_reference,
    validate_response,
)


class JobAsking:
    def __init__(self, api):
        self.client = api

    @rate_limiter
    def get(
        self,
        board_key: str,
        questions: t.List[str],
        reference: t.Optional[str] = None,
        key: t.Optional[str] = None,
    ) -> t.Dict[str, t.Any]:
        """
        Ask a question to a Job indexed in a Board. This endpoint allows asking a
        question based on a Job object.

        Args:
            board_key:      <str>
                            The key of the Board associated to the job
            questions:      <list[str]>
                            Questions based on the queried job
            reference:      <Optional[str]>
                            The Job reference chosen by the customer
            key:            <Optional[str]>
                            The Job unique identifier

        Returns:
            `/job/asking` response
        """

        params = dict(
            board_key=validate_key("Board", board_key, regex=KEY_REGEX),
            reference=validate_reference(reference),
            key=validate_key("Job", key, regex=KEY_REGEX),
            questions=questions,
        )

        response = self.client.get("job/asking", query_params=params)

        return validate_response(response)
