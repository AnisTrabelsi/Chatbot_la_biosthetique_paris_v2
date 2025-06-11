import uuid
import os
from sqlalchemy import Column, String, Float, Boolean
from app.db.base import Base
from cryptography.fernet import Fernet

# Clé Fernet pour chiffrer le token Portatour
# À générer une seule fois et mettre dans .env : FERNET_KEY
fernet_key = os.getenv("FERNET_KEY", Fernet.generate_key().decode())
fernet = Fernet(fernet_key.encode())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    portatour_token_enc = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    sector = Column(String, nullable=True)
    onboarded = Column(Boolean, default=False)

    @property
    def portatour_token(self) -> str | None:
        if self.portatour_token_enc:
            return fernet.decrypt(self.portatour_token_enc.encode()).decode()
        return None

    @portatour_token.setter
    def portatour_token(self, value: str):
        self.portatour_token_enc = fernet.encrypt(value.encode()).decode()
