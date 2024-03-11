import typing as t

from ..core.rate_limit import rate_limiter
from ..core.validation import validate_key, validate_response

API_SECRET_REGEX = r"^ask[rw]?_[0-9a-f]{32}$"


class Auth:
    def __init__(self, api):
        self.client = api

    @rate_limiter
    def get(self) -> t.Dict[str, t.Any]:
        """
        Try your API Keys. This endpoint allows you to learn how to add the right
        information to your API calls, so you can make them.

        Args:
            api_user:       <str>
                            Your HrFlow.ai account's email.
            api_secret:     <str>
                            Your API Key.

        Returns:
            `/auth` response
        """

        validate_key(
            "api_secret",
            self.client.auth_header.get("X-API-KEY"),
            regex=API_SECRET_REGEX,
        )

        response = self.client.get("auth")

        return validate_response(response)
