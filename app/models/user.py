import uuid
from sqlalchemy import Column, String, Float, Boolean
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    portatour_token = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    sector = Column(String, nullable=True)
    onboarded = Column(Boolean, default=False)
