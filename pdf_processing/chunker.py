from typing import List
import re


class TextChunker:
    """
    Sentence-aware chunking for RAG.
    Preserves sentence boundaries while maintaining overlap.
    """

    @staticmethod
    def chunk(
        text: str,
        chunk_size: int = 900,
        overlap: int = 150
    ) -> List[str]:

        if not text:
            return []

        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)

        chunks = []
        current_chunk = ""

        for sentence in sentences:

            # If sentence itself is huge, split it
            if len(sentence) > chunk_size:

                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""

                for i in range(0, len(sentence), chunk_size - overlap):
                    chunks.append(sentence[i:i + chunk_size])

                continue

            # Add sentence if it fits
            if len(current_chunk) + len(sentence) + 1 <= chunk_size:

                current_chunk += " " + sentence

            else:

                chunks.append(current_chunk.strip())

                # Character overlap
                overlap_text = current_chunk[-overlap:]

                current_chunk = overlap_text + " " + sentence

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks