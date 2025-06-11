import uuid
from datetime import datetime
from sqlalchemy import Column, String, JSON, DateTime
from app.db.base import Base

class LeadEnrichment(Base):
    __tablename__ = "lead_enrichments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, nullable=False, index=True)
    data = Column(JSON, nullable=False)
    score = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
