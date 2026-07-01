import os
import pickle

import faiss
import numpy as np


class FAISSService:

    def __init__(self):

        self.index_dir = "data/faiss"

        os.makedirs(
            self.index_dir,
            exist_ok=True
        )

        self.index_path = os.path.join(
            self.index_dir,
            "index.faiss"
        )

        self.metadata_path = os.path.join(
            self.index_dir,
            "metadata.pkl"
        )

        self.dimension = 384

        # Load existing index if available
        if (
            os.path.exists(self.index_path)
            and os.path.exists(self.metadata_path)
        ):

            self.index = faiss.read_index(
                self.index_path
            )

            with open(
                self.metadata_path,
                "rb"
            ) as file:

                self.metadata = pickle.load(file)

            print("FAISS index loaded.")

        else:

            self.index = faiss.IndexFlatL2(
                self.dimension
            )

            self.metadata = []

            print("New FAISS index created.")

    # =====================================================
    # RESET INDEX
    # =====================================================

    def reset(self):

        self.index = faiss.IndexFlatL2(
            self.dimension
        )

        self.metadata = []

        self.save()

        print("FAISS index reset.")

    # =====================================================
    # ADD EMBEDDINGS
    # =====================================================

    def add(
        self,
        embeddings,
        chunks,
        paper_id
    ):

        embeddings = embeddings.astype(
            np.float32
        )

        self.index.add(
            embeddings
        )

        for chunk in chunks:

            self.metadata.append({

                "paper_id": paper_id,

                "text": chunk

            })

        self.save()

    # =====================================================
    # SAVE INDEX
    # =====================================================

    def save(self):

        faiss.write_index(
            self.index,
            self.index_path
        )

        with open(
            self.metadata_path,
            "wb"
        ) as file:

            pickle.dump(
                self.metadata,
                file
            )

        print("FAISS index saved.")

    # =====================================================
    # SEARCH
    # =====================================================

    def search(
        self,
        query_embedding,
        k=5
    ):

        query_embedding = query_embedding.astype(
            np.float32
        )

        # Retrieve more candidates than needed
        distances, indices = self.index.search(
            query_embedding,
            k * 2
        )

        results = []

        seen = set()

        for idx in indices[0]:

            if idx >= len(self.metadata):
                continue

            item = self.metadata[idx]

            text = item["text"].strip()

            # Skip very small chunks
            if len(text) < 120:
                continue

            # Remove duplicate chunks
            if text in seen:
                continue

            seen.add(text)

            results.append(item)

            if len(results) >= k:
                break

        return results