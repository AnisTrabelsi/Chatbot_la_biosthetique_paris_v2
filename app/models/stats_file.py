from sqlalchemy import Column, String, Text
from app.db.base import Base


class StatsFile(Base):
    """
    Ligne d’un bilan Excel stockée brute en JSON.
    """

    __tablename__ = "stats_files"

    id = Column(String, primary_key=True)
    kdnr = Column(String, index=True, nullable=False)
    raw = Column(Text, nullable=False)            # ← ajouté
