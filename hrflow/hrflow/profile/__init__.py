"""Profile related calls."""

from .asking import ProfileAsking
from .attachment import ProfileAttachments
from .embedding import ProfileEmbedding
from .parsing import ProfileParsing
from .reasoning import ProfileReasoning
from .revealing import ProfileRevealing
from .scoring import ProfileScoring
from .searching import ProfileSearching
from .storing import ProfileStoring
from .unfolding import ProfileUnfolding


class Profile(object):
    def __init__(self, client):
        """
        Initialize Profile object with hrflow client.

        Args:
            client: hrflow client instance <hrflow object>

        Returns
            Profile instance object.

        """
        self.client = client
        self.asking = ProfileAsking(self.client)
        self.attachment = ProfileAttachments(self.client)
        self.parsing = ProfileParsing(self.client)
        self.storing = ProfileStoring(self.client)
        self.embedding = ProfileEmbedding(self.client)
        self.revealing = ProfileRevealing(self.client)
        self.scoring = ProfileScoring(self.client)
        self.searching = ProfileSearching(self.client)
        self.reasoning = ProfileReasoning(self.client)
        self.unfolding = ProfileUnfolding(self.client)
