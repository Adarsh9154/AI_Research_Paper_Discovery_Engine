from datetime import datetime
from . import db


class Chunk(db.Model):

    __tablename__ = "chunks"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    paper_id = db.Column(
        db.String(255),
        nullable=False
    )

    chunk_index = db.Column(
        db.Integer,
        nullable=False
    )

    chunk_text = db.Column(
        db.Text,
        nullable=False
    )

    vector_id = db.Column(
        db.Integer,
        nullable=False,
        unique=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )