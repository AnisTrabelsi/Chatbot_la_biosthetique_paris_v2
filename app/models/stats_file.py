import uuid
from sqlalchemy import Column, String, JSON, ForeignKey
from app.db.base import Base

class StatsFile(Base):
    __tablename__ = "stats_files"

    id: str = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    kdnr: str = Column(String, ForeignKey("clients.kdnr"), nullable=False, index=True)

    # ➜ nouvelle colonne pour stocker la ligne Excel brute
    raw: dict | None = Column(JSON, nullable=True)          # <— AJOUT
