import typing as t

from ..core.rate_limit import rate_limiter
from ..core.validation import (

    KEY_REGEX,
    validate_key,
    validate_response,
    validate_score,
)
class JobUpskilling:
    def __init__(self, api):
        self.client = api

    @rate_limiter
    def get(
        self,
        board_key: str,
        job_key: str,
        source_key: str,
        profile_key: str,
        score: float,
        output_lang: str = "en",
    ) -> t.Dict[str, t.Any]:
        """
        🧠Get the SWOT explaining a Job recommendation for a Profile.
        (https://api.hrflow.ai/v1/job/upskilling)
        Args:
            source_key:    <str>
                            The key of the Source associated to the profile.
            profile_key:   <str>
                            The Profile unique identifier.
            board_key:     <str>
                            The key of the Board associated to the job.
            job_key:       <str>
                            The Job unique identifier.
            score:         <float>
                            Matching score of the Job according to the Profile. The Score value is between 0 and 1.
            output_lang:   <str>
                            The language of the output. Default is 'en'.

        Returns:
            `/job/upskilling` response
        """

        params = dict(
            source_key=validate_key("Source", source_key, regex=KEY_REGEX),
            profile_key=validate_key("Profile", profile_key, regex=KEY_REGEX),
            board_key=validate_key("Board", board_key, regex=KEY_REGEX),
            job_key=validate_key("Job", job_key, regex=KEY_REGEX),
            score=validate_score(score),
            output_lang=output_lang,
        )

        response = self.client.get("job/upskilling", query_params=params)

        return validate_response(response)