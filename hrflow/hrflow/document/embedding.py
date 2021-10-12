from ..utils import validate_value, ITEM_TYPE, validate_response


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
            "item_type": validate_value(item_type, ITEM_TYPE, "item type"),
            "item": item,
            "return_sequences": return_sequences
        }
        response = self.client.post('document/embedding', json=payload)

        return validate_response(response)
