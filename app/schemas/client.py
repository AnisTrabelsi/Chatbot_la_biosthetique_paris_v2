from pydantic import BaseModel, Field, constr
from datetime import datetime
from pydantic import constr

# Exemple de contrainte téléphone E.164 (commencera par + suivis de 8-15 chiffres)
PhoneE164 = constr(pattern=r"^\+[1-9]\d{7,14}$")

class ClientCreate(BaseModel):
    kdnr: str = Field(..., min_length=1)
    name: str
    phone: PhoneE164 | None = None  # facultatif

class ClientRead(ClientCreate):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True
