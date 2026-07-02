from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingService:
    """
    Generates embeddings for text chunks using
    Sentence Transformers.
    """

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Embedding model loaded.")

    def generate(self, texts):

        if isinstance(texts, str):
            texts = [texts]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True
        )

        return embeddings.astype(np.float32)