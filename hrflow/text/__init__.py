"""Profile related calls."""

from .embedding import TextEmbedding
from .imaging import TextImaging
from .linking import TextLinking
from .ocr import TextOCR
from .parsing import TextParsing
from .tagging import TextTagging


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
        self.tagging = TextTagging(self.client)
        self.ocr = TextOCR(self.client)
        self.imaging = TextImaging(self.client)
