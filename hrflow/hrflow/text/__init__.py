"""Profile related calls."""
from .parsing import TextParsing
from .linking import TextLinking
from .revealing import TextRevealing
from .embedding import TextEmbedding
from .tagging import TextTagging
from .ocr import TextOCR
from .imaging import TextImaging


class Text(object):
    """Text related calls."""

    def __init__(self, client):
        """
        Initialize Profile object with hrflow client.

        Args:
            client: hrflow client instance <hrflow object>

        Returns
            Profile instance object.

        """
        self.client = client
        self.parsing = TextParsing(self.client)
        self.linking = TextLinking(self.client)
        self.embedding = TextEmbedding(self.client)
        self.revealing = TextRevealing(self.client)
        self.tagging = TextTagging(self.client)
        self.ocr = TextOCR(self.client)
        self.imaging = TextImaging(self.client)
