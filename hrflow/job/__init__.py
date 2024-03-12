from .asking import JobAsking
from .embedding import JobEmbedding
from .parsing import JobParsing
from .reasoning import JobReasoning
from .scoring import JobScoring
from .searching import JobSearching
from .storing import JobStoring


class Job:
    def __init__(self, client):
        self.client = client
        self.asking = JobAsking(self.client)
        self.parsing = JobParsing(self.client)
        self.embedding = JobEmbedding(self.client)
        self.searching = JobSearching(self.client)
        self.scoring = JobScoring(self.client)
        self.reasoning = JobReasoning(self.client)
        self.storing = JobStoring(self.client)
