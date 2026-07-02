from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .paper import Paper   # noqa: E402  (must import after db is defined)
from .chunk import Chunk   # noqa: E402

__all__ = ["db", "Paper", "Chunk"]
