from .validator import validate_source_id, validate_profile_id, validate_profile_reference, validate_job_id\
    , validate_job_reference


class ProfileRevealing():
    """Manage revealing related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def get(self, source_id=None, profile_id=None, profile_reference=None, job_id=None, job_reference=None):
        """
        Retrieve the revealing information.

        Args:
            source_id:          <string>
                                source id
            profile_id:         <string>
                                profile id
            profile_reference:  <string>
                                profile_reference
            job_id:             <string>
                                job id
            job_reference:      <string>
                                job_reference

        Returns
            Revealing information
        """
        query_params = {"source_id": validate_source_id(source_id)}
        if profile_id:
            query_params["profile_id"] = validate_profile_id(profile_id)
        if profile_reference:
            query_params["profile_reference"] = validate_profile_reference(profile_reference)
        if job_id:
            query_params["job_id"] = validate_job_id(job_id)
        if job_reference:
            query_params["job_reference"] = validate_job_reference(job_reference)
        response = self.client.get('profile/revealing', query_params)
        return response.json()
