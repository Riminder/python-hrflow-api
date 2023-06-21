"""Profile related calls."""
from .attachment import ProfileAttachments
from .parsing import ProfileParsing
from .storing import ProfileStoring
from .revealing import ProfileRevealing
from .embedding import ProfileEmbedding
from .searching import ProfileSearching
from .scoring import ProfileScoring
from .reasoning import ProfileReasoning


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
        self.attachment = ProfileAttachments(self.client)
        self.parsing = ProfileParsing(self.client)
        self.storing = ProfileStoring(self.client)
        self.embedding = ProfileEmbedding(self.client)
        self.revealing = ProfileRevealing(self.client)
        self.scoring = ProfileScoring(self.client)
        self.searching = ProfileSearching(self.client)
        self.reasoning = ProfileReasoning(self.client)
