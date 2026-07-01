import re


class TextCleaner:
    """
    Cleans extracted PDF text before chunking.
    """

    @staticmethod
    def clean(text: str) -> str:

        if not text:
            return ""

        # Normalize line endings
        text = text.replace("\r", "\n")

        # Replace tabs with spaces
        text = text.replace("\t", " ")

        # Remove multiple spaces
        text = re.sub(r"[ ]+", " ", text)

        # Remove multiple blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Remove leading/trailing whitespace
        text = text.strip()

        return text