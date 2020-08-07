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
