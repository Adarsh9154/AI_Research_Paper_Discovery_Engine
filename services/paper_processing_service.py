from pdf_processing.downloader import PDFDownloader
from pdf_processing.extractor import PDFExtractor
from pdf_processing.cleaner import TextCleaner
from pdf_processing.chunker import TextChunker

from embeddings.embedding_service import EmbeddingService
from vectorstore.faiss_service import FAISSService

from utils.logger import Logger


class PaperProcessingService:
    """
    Complete Research Paper Processing Pipeline

    PDF
      ↓
    Download
      ↓
    Extract Text
      ↓
    Clean Text
      ↓
    Create Chunks
      ↓
    Generate Embeddings
      ↓
    Store in FAISS
    """

    def __init__(self):

        self.downloader = PDFDownloader()

        self.embedding_service = EmbeddingService()

        self.faiss_service = FAISSService()

    def process(
        self,
        paper_id: str,
        pdf_url: str
    ) -> dict:

        print("\n==============================")
        print("Starting Paper Processing")
        print("==============================")

        Logger.info("Starting Paper Processing")

        # =====================================
        # STEP 1 : DOWNLOAD PDF
        # =====================================

        print("\n[1/6] Downloading PDF...")

        Logger.info("Downloading PDF")

        pdf_path = self.downloader.download(
            paper_id=paper_id,
            pdf_url=pdf_url
        )

        # =====================================
        # STEP 2 : EXTRACT TEXT
        # =====================================

        print("[2/6] Extracting Text...")

        Logger.info("Extracting Text")

        raw_text = PDFExtractor.extract(
            pdf_path
        )

        # =====================================
        # STEP 3 : CLEAN TEXT
        # =====================================

        print("[3/6] Cleaning Text...")

        Logger.info("Cleaning Text")

        clean_text = TextCleaner.clean(
            raw_text
        )

        # =====================================
        # STEP 4 : CREATE CHUNKS
        # =====================================

        print("[4/6] Creating Chunks...")

        Logger.info("Creating Chunks")

        chunks = TextChunker.chunk(
            clean_text
        )

        Logger.info(
            f"Created {len(chunks)} chunks."
        )

        print(f"Created {len(chunks)} chunks.")

        # =====================================
        # STEP 5 : GENERATE EMBEDDINGS
        # =====================================

        print("[5/6] Generating Embeddings...")

        Logger.info("Generating Embeddings")

        embeddings = self.embedding_service.generate(
            chunks
        )

        Logger.info(
            f"Generated {len(embeddings)} embeddings."
        )

        # =====================================
        # STEP 6 : SAVE TO FAISS
        # =====================================

        print("[6/6] Saving to FAISS...")

        Logger.info("Resetting FAISS Index")

        self.faiss_service.reset()

        Logger.info("Saving Embeddings")

        self.faiss_service.add(
            embeddings=embeddings,
            chunks=chunks,
            paper_id=paper_id
        )

        Logger.info("Paper Processing Completed")

        print("\n✅ Paper Processing Completed.")

        return {

            "paper_id": paper_id,

            "pdf_path": pdf_path,

            "raw_text": raw_text,

            "clean_text": clean_text,

            "chunks": chunks,

            "embeddings": embeddings

        }