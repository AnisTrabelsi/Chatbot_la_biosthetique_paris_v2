import uuid
from sqlalchemy import Column, String
from app.db.base import Base

class Client(Base):
    __tablename__ = "clients"

    id        = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name      = Column(String, nullable=False)
    phone_e164 = Column(String, unique=True, nullable=False)   # +33612345678
    kdnr      = Column(String(8), unique=True, nullable=True)   # 6-8 chiffres
    siret     = Column(String(14), unique=True, nullable=True)  # 14 chiffres
