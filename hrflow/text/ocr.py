from ..core.rate_limit import rate_limiter
from ..core.validation import validate_response


class TextOCR:
    "Manage Text extraction from documents using in-house advance OCR related calls."

    def __init__(self, api):
        """Init."""
        self.client = api

    @rate_limiter
    def post(self, file):
        """
        This endpoint allows you to extract a the text from a document across all
        formats (pdf, docx, png, and more).
        Supported extensions by the Profile Parsing API are .pdf, .png, .jpg, .jpeg,
        .bmp, .doc, .docx, .odt, .rtf, .odp, ppt, and .pptx.

        Args:
            file:                   <binary file>
                                    binary file content
        Returns
            Extracted text along with pages, blocks and more

        """
        response = self.client.post("text/ocr", files={"file": file})
        return validate_response(response)
