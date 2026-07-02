from models import db, Chunk


class ChunkRepository:

    @staticmethod
    def save_chunks(paper_id, chunks, start_vector_id):

        chunk_models = []

        for index, chunk in enumerate(chunks):

            chunk_model = Chunk(
                paper_id=paper_id,
                chunk_index=index,
                chunk_text=chunk,
                vector_id=start_vector_id + index
            )

            db.session.add(chunk_model)

            chunk_models.append(chunk_model)

        db.session.commit()

        return chunk_models

    @staticmethod
    def get_by_vector_id(vector_id):

        return Chunk.query.filter_by(
            vector_id=vector_id
        ).first()

    @staticmethod
    def get_by_paper_id(paper_id):

        return Chunk.query.filter_by(
            paper_id=paper_id
        ).all()