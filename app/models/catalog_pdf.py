import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, Integer
from app.db.base import Base

class CatalogPDF(Base):
    __tablename__ = "catalog_pdfs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    doc_type = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    version = Column(Integer, default=1)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    meta = Column("metadata", JSON, nullable=True)  # <— renommer en meta
