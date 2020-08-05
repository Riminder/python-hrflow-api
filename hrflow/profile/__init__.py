"""Profile related calls."""
from .attachment import ProfileAttachments
from .parsing import ProfileParsing
from .indexing import ProfileIndexing
from .revealing import ProfileRevealing
from .embedding import ProfileEmbedding
from .searching import ProfileSearching
from .scoring import ProfileScoring
from .reasoning import ProfileReasoning


class Profile(object):
    """
    Class that interacts with hrflow API profiles endpoint.

    Usage example:

    >>> from hrflow import client
    >>> from hrflow.profile import Profile
    >>> client = client(api_key="YOUR_API_KEY")
    >>> profile = Profile(self.client)
    >>> result = profile.get_profiles(source_ids=["5823bc959983f7a5925a5356020e60d605e8c9b5"])
    >>> print(result)
    {
        "code": 200,
        "message": "OK",
        "data": {
            "page": 1,
            "maxPage": 3,
            "count_profiles": 85,
            "profiles": [
            {
                "profile_id": "215de6cb5099f4895149ec0a6ac91be94ffdd246",
                "profile_reference": "49583",
                ...
    """

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
        self.indexing = ProfileIndexing(self.client)
        self.embedding = ProfileEmbedding(self.client)
        self.revealing = ProfileRevealing(self.client)
        self.scoring = ProfileScoring(self.client)
        self.searching = ProfileSearching(self.client)
        self.reasoning = ProfileReasoning(self.client)
