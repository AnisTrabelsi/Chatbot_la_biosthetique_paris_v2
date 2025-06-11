import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean
from app.db.base import Base

class WASession(Base):
    __tablename__ = "wa_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    phone_number = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_closed = Column(Boolean, default=False)
