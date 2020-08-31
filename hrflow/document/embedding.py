
import numpy as np

dfloat32 = np.dtype('>f4')


class DocumentEmbedding():
    """Manage embedding related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def post(self, item_type, item, return_sequences=False):
        """
        Retrieve Embedding.

        Args:
            item_type:             <string>
                                   item_type
            item:                  <object>
                                   item
            return_sequences:      <bool>
                                   return_sequences
        Returns
            Embedding

        """
        payload = {
            "item_type": item_type,
            "item": item,
            "return_sequences": return_sequences
        }
        response = self.client.post('document/embedding', json=payload)

        return response.json()
