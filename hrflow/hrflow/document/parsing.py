import os
import json

from ..utils import get_item, validate_key, validate_reference, get_files_from_dir


class DocumentParsing():
    """Manage parsing related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def post(self):
        """
        Post Parsing information.

        Returns
            Get information

        """
        return
