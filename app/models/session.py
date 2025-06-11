import uuid
from datetime import datetime, UTC

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class WASession(Base):
    """
    Session WhatsApp liée à un commercial.
    """

    __tablename__ = "wa_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    phone_number = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    is_closed = Column(Boolean, default=False)

    # Rattachement facultatif à un utilisateur
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="wa_sessions", lazy="joined")
