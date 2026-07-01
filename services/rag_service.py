from embeddings.embedding_service import EmbeddingService
from vectorstore.faiss_service import FAISSService

from llm.groq_client import GroqClient
from llm.prompt_template import build_prompt


class RAGService:

    def __init__(self):

        self.embedder = EmbeddingService()

        self.faiss = FAISSService()

        self.llm = GroqClient()

    def ask(self, question: str):

        # Generate query embedding
        query_embedding = self.embedder.generate(
            [question]
        )

        # Search FAISS
        results = self.faiss.search(
            query_embedding=query_embedding,
            k=6
        )

        print("\n" + "=" * 80)
        print("RETRIEVED CHUNKS")
        print("=" * 80)

        for i, result in enumerate(results, start=1):

            print(f"\nChunk {i}")
            print("-" * 60)
            print(result["text"][:500])

        # Build context
        context = "\n\n".join(
            result["text"]
            for result in results
        )

        # Build prompt
        prompt = build_prompt(
            context=context,
            question=question
        )

        # Generate answer
        answer = self.llm.generate(
            prompt
        )

        return answer