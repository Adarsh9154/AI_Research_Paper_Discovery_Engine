from models import db, Paper


class PaperRepository:

    @staticmethod
    def save(paper_data):

        existing_paper = Paper.query.filter_by(
            id=paper_data["id"]
        ).first()

        if existing_paper:
            return existing_paper

        publication_year = paper_data.get("publication_year")

        paper = Paper(
            id=paper_data["id"],
            title=paper_data["title"],
            authors=paper_data["authors"],
            abstract=paper_data.get("abstract"),
            publication_year=(
                int(publication_year) if publication_year else None
            ),
            source=paper_data.get("source", "arXiv"),
            pdf_url=paper_data.get("pdf_url")
        )

        db.session.add(paper)
        db.session.commit()

        return paper

    @staticmethod
    def save_many(papers):

        saved_papers = []

        for paper in papers:
            saved_papers.append(
                PaperRepository.save(paper)
            )

        return saved_papers

    @staticmethod
    def get_by_id(paper_id):

        return Paper.query.filter_by(
            id=paper_id
        ).first()

    @staticmethod
    def get_all():

        return Paper.query.all()