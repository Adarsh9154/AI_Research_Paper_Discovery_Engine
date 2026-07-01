import fitz


class PDFExtractor:
    """
    Extracts text from PDF files using PyMuPDF.
    """

    @staticmethod
    def extract(pdf_path: str) -> str:

        document = fitz.open(pdf_path)

        pages = []

        try:

            for page in document:

                text = page.get_text("text")

                if text:
                    pages.append(text)

        finally:

            document.close()

        return "\n".join(pages)