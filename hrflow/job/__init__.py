from .parsing import JobParsing
from .indexing import JobIndexing
from .embedding import JobEmbedding
from .searching import JobSearching
from .scoring import JobScoring
from .reasoning import JobReasoning


class Job(object):

    def __init__(self, client):
        self.client = client
        self.parsing = JobParsing(self.client)
        self.indexing = JobIndexing(self.client)
        self.embedding = JobEmbedding(self.client)
        self.searching = JobSearching(self.client)
        self.scoring = JobScoring(self.client)
        self.reasoning = JobReasoning(self.client)

    def add_json(self, name, agent_id, job_reference, job_labels=[], job_metadatas=[], **kwargs):
        """
                Use the api to add a new job using json_data.

                Args:
                    name:               <string>
                                        name
                    agent_id:           <string>
                                        agent_id
                    job_reference:      <string>
                                        job_reference
                    job_labels:         <list>
                                        job_labels
                    job_metadatas:      <list>
                                        job_metadatas
                    agent_id:           <string>
                                        agent_id
                    kwargs:             additional information

                Returns
                    201 if the job is successfully created
        """
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
