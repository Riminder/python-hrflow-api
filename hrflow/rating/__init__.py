from ..core.rate_limit import rate_limiter
from ..core.validation import validate_response


class Rating:
    def __init__(self, client):
        self.client = client

    @rate_limiter
    def get(
        self,
        role,
        source_keys=None,
        source_key=None,
        profile_key=None,
        profile_reference=None,
        board_keys=None,
        board_key=None,
        job_key=None,
        job_reference=None,
        return_profile=False,
        return_author=False,
        page=1,
        limit=30,
        order_by="desc",
        sort_by="scoring",
        created_at_min=None,
        created_at_max=None,
        location_lat=None,
        location_lon=None,
        location_distance=None,
        use_location_address=None,
        use_location_experience=None,
        use_location_education=None,
        experiences_duration_min=None,
        experiences_duration_max=None,
        educations_duration_min=None,
        educations_duration_max=None,
    ):
        """
        This endpoint allows you to retrieve the list of ratings.
        Visit : https://developers.hrflow.ai/reference for more information.

        Retrieve Ratings Associated with a Specific Profile or Job
            - To filter by a specific profile, include the parameters (source_key,
                profile_key//profile_reference) and leave source_keys empty.
            - To filter by a specific job, include the parameters (board_key,
                job_key//job_reference) and leave board_keys empty.

        Retrieve Ratings Associated with a Specific List of Profiles or Jobs
            - To filter ratings based on a list of profiles within a list of sources,
                include the parameter source_keys and leave (source_key,
                profile_key//profile_reference) empty.
            - To filter ratings based on a list of jobs within a list of boards,
                include the parameter board_keys and leave (board_key,
                job_key//job_reference) empty.
        """
        args = locals()
        params = {}

        for arg, value in args.items():
            if value is not None and arg != "self":
                params[arg] = value

        response = self.client.get(resource_endpoint="ratings", query_params=params)

        return validate_response(response)

    @rate_limiter
    def post(
        self,
        score,
        role,
        board_key,
        source_key,
        job_key=None,
        job_reference=None,
        profile_key=None,
        profile_reference=None,
        author_email=None,
        comment=None,
        created_at=None,
    ):
        """
        This endpoint allows you to rate a Profile (resp. a Job) for Job (resp. a
        Profile)
        as a recruiter (resp. a candidate) with a score between 0 and 1.
        Visit : https://developers.hrflow.ai/reference for more information.

        The job_key and the job_reference cannot be null at the same time in the
        Request Parameters.
        The same for the profile_key and profile_reference.

        Args:
            score:                  <float>
                                    The score is an evaluation fit between 0 to 1 .
                                    If you're using stars in your system please use
                                    the following conversion:
                                    5 stars = 1.0 , 4 stars=0.8 , 3 stars=0.6, 2
                                    stars=0.4, 1 star= 0.2 .
            role:                   <string>
                                    Role of the user rating the job role in
                                    {recruiter, candidate, employee, manager}.
            board_key:              <string>
                                    The key of Board attached to the given Job.
            source_key:             <string>
                                    The key of Source attached to the given Profile.
            job_key:                <string>
                                    job identifier (key)
            job_reference:          <string>
                                    The Job reference chosen by the customer or an
                                    external system.
                                    If you use the job_key you do not need to specify
                                    the job_reference and vice versa.
            profile_key:            <string>
                                    profile identifier (key)
            profile_reference:      <string>
                                    The Profile reference chosen by the customer or an
                                    external system.
                                    If you use the profile_key you do not need to
                                    specify the profile_reference and vice versa.
            author_email:           <string>
                                    author email
            comment:                <string>
                                    comment
            created_at:             <string>
                                    ISO Date of the rating.
                                    Format : yyyy-MM-dd'T'HH:mm:ss.SSSXXX — for
                                    example, "2000-10-31T01:30:00.000-05:00"
                                    It associates a creation date to the profile (ie:
                                    this can be for example the original date of the
                                    application of the profile).
                                    If not provided the creation date will be now by
                                    default.
        """

        args = locals()
        body = {}

        for arg, value in args.items():
            if value is not None and arg != "self":
                body[arg] = value

        # Underlying resource : POST /rating
        response = self.client.post(resource_endpoint="rating", json=body)
        return validate_response(response)
