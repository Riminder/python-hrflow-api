import json
from .validator import validate_source_ids, validate_job_id, validate_stage


class ProfileScoring():
    """Manage stage related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def search(self, source_ids=None, job_id=None, stage=None, limit=10, use_agent=1):
        """
        Retrieve the scoring information.

        Args:
            source_ids:         <list>
                                source ids
            job_id:             <string>
                                job id
            stage:              <string>
                                stage
            limit:              <int>
                                limit
            use_agent:          <int>
                                use_agent

        Returns
            parsing information

        """
        query_params = {"source_ids": json.dumps(validate_source_ids(source_ids))}
        if job_id:
            query_params["job_id"] = validate_job_id(job_id)
        if stage:
            query_params["stage"] = validate_stage(stage)
        query_params["limit"] = limit
        query_params["use_agent"] = use_agent
        response = self.client.get('profiles/scoring', query_params)
        print(response)
        return response.json()
