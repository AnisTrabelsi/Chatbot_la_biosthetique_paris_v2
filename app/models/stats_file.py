import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON
from app.db.base import Base

class StatsFile(Base):
    __tablename__ = "stats_files"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    kdnr = Column(String, index=True, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    data = Column(JSON, nullable=False)
