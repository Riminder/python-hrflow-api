from .validator import validate_profile_id, validate_job_id, validate_stage


class ProfileFeedback():
    """Manage stage related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def set(self, profile_id=None, job_id=None, stage=None, rating=None):
        """
        Edit the profile feed back given a job.

        Args:
            profile_id:             <string>
                                    profile id
            job_id:                 <string>
                                    job id
            stage:                  <string>
                                    profiles' stage associated to the job (new, yes, later, or no)
            rating:                 <float>
                                    rting.

        Returns
            Response that contains code 201 if successful
            Other status codes otherwise.

        """
        data = {"profile_id": validate_profile_id(profile_id), "job_id": validate_job_id(job_id),
                "stage": validate_stage(stage), 'rating': rating}
        response = self.client.patch('profile/action', data=data)
        return response.json()
