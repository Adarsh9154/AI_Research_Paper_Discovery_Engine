from embeddings.embedding_service import EmbeddingService
from vectorstore.faiss_service import FAISSService
from repositories.chunk_repository import ChunkRepository


class SemanticSearchService:

    def __init__(self):

        self.embedding_service = EmbeddingService()

        self.faiss_service = FAISSService()

    def search(self, query, top_k=5):

        query_embedding = self.embedding_service.generate_embedding(
            query
        )

        distances, indices = self.faiss_service.search(
            query_embedding,
            k=top_k
        )

        results = []

        for vector_id in indices[0]:

            chunk = ChunkRepository.get_by_vector_id(
                int(vector_id)
            )

            if chunk:

                results.append({

                    "paper_id": chunk.paper_id,

                    "vector_id": chunk.vector_id,

                    "chunk_index": chunk.chunk_index,

                    "text": chunk.chunk_text

                })

        return results