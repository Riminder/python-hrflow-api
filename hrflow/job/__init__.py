from .parsing import JobParsing
from .scoring import JobScoring
from .validator import validate_job_id, validate_job_reference


class Job(object):

    def __init__(self, client):
        self.client = client
        self.parsing = JobParsing(self.client)
        self.scoring = JobScoring(self.client)

    def add_json(self, name, agent_id, job_reference, job_labels=[], job_metadatas=[], **kwargs):
        """Use the api to add a new job using json_data."""
        payload = {
            'name': name,
            'agent_id': agent_id,
            "job_reference": job_reference,
            "job_labels": job_labels,
            "job_metadatas": job_metadatas
        }
        data = {**payload, **kwargs}
        response = self.client.post("job", data=data)
        return response.json()

    def search(self, name=None):
        query_params = {}
        if name:
            query_params['name'] = name
        response = self.client.get("jobs/searching", query_params)
        return response.json()

    def get(self, job_id=None, job_reference=None):
        query_params = {}
        if job_id:
            query_params["job_id"] = validate_job_id(job_id)
        if job_reference:
            query_params["job_reference"] = validate_job_reference(job_reference)

        response = self.client.get('job', query_params)
        return response.json()
