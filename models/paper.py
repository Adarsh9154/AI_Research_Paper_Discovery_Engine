from datetime import datetime

from . import db


class Paper(db.Model):
    """
    Persisted Paper record.

    Note: providers/arxiv_provider.py builds Paper(...) instances purely
    as in-memory objects (never added to a db.session) whenever it just
    needs a lightweight value object to pass around the app. Because this
    is a normal SQLAlchemy declarative model, that still works fine --
    you only touch the database when you actually call
    db.session.add(...)/commit() (see repositories/paper_repository.py).
    """

    __tablename__ = "papers"

    id = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.Text, nullable=False)
    authors = db.Column(db.Text, nullable=False)  # comma-separated string
    abstract = db.Column(db.Text)
    pdf_url = db.Column(db.String(500))
    publication_year = db.Column(db.Integer)
    source = db.Column(db.String(50), default="arXiv")
    doi = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Paper {self.id!r} {self.title!r}>"
