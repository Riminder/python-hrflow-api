from .parsing import JobParsing
from .embedding import JobEmbedding
from .searching import JobSearching
from .scoring import JobScoring
from .reasoning import JobReasoning
from .storing import JobStoring


class Job:
    def __init__(self, client):
        self.client = client
        self.parsing = JobParsing(self.client)
        self.embedding = JobEmbedding(self.client)
        self.searching = JobSearching(self.client)
        self.scoring = JobScoring(self.client)
        self.reasoning = JobReasoning(self.client)
        self.storing = JobStoring(self.client)
