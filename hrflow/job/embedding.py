from .validator import validate_job_id, validate_job_reference


class JobEmbedding():
    """Manage embedding related job calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def get(self, job_id, job_reference=None):
        """
        Retrieve the embedding information.

        Args:
            job_id:                 <string>
                                    job_id id
            job_reference:          <string>
                                    job_reference id
        Returns
            embedding information

        """
        query_params = {}
        query_params["job_id"] = validate_job_id(job_id)
        if job_reference:
            query_params["job_reference"] = validate_job_reference(job_reference)
        response = self.client.get('job/embedding', query_params)
        return response.json()
