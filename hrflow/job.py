import json

class Job(object):

    def __init__(self, client):
        self.client = client
        self.parsing = JobParsing(self.client)
        self.scoring = JobScoring(self.client)
        self.json = JobJson(self.client)

    def list(self, name=None):
        query_params = {}
        if name:
            query_params['name'] = name
        response = self.client.get("jobs/searching", query_params)
        return response.json()

    def get(self, job_id=None, job_reference=None):
        query_params = {}
        if job_id:
            query_params["job_id"] = _validate_job_id(job_id)
        if job_reference:
            query_params["job_reference"] = _validate_job_reference(job_reference)

        response = self.client.get('job', query_params)
        return response.json()


class JobParsing():
    """Manage parsing related job calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def get(self, job_id=None, job_reference=None):
        """
        Retrieve the parsing information.

        Args:
            job_id:                 <string>
                                    job_id id
            job_reference:          <string>
                                    job_reference id

        Returns
            parsing information

        """
        query_params = {}
        query_params["job_id"] = _validate_job_id(job_id)
        if job_reference:
            query_params["job_reference"] = _validate_job_reference(job_reference)
        response = self.client.get('job/parsing', query_params)
        return response.json()


class JobScoring():
    """Manage job related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    # TODO add job scoring
    def list(self):
        return


class JobJson():
    """Gathers route about structured job."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def add(self, name, agent_id, job_reference, job_json, job_labels=[], job_metadatas=[], timestamp_reception=None):
        """Use the api to add a new job using json_data."""
        payload = {
            'name': name,
            'agent_id': agent_id,
            "job_reference": job_reference,
            "job_json": job_json,
            "job_labels": job_labels,
            "job_metadatas": job_metadatas
        }

        # some enrichement for profile_json
        if timestamp_reception is not None:
            payload['timestamp_reception'] = _validate_timestamp(timestamp_reception, 'timestamp_reception')

        data = {'data': json.dumps(payload)}

        response = self.client.post("job", data=data)
        return response.json()


def _validate_job_id(value):
    if not isinstance(value, str) and value is not None:
        raise TypeError("job_id must be string")
    return value


def _validate_job_reference(value, acceptnone=True):
    if value is None:
        if acceptnone is False:
            raise TypeError("job_reference must not be None")
        else:
            return value

def _validate_timestamp(value, var_name="timestamp"):
    if isinstance(value, int) or isinstance(value, float):
        return str(value)
    if not isinstance(value, str) and value is not None:
        raise TypeError("{} must be string or a int".format(var_name))
    return value