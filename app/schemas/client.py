# app/schemas/client.py
from pydantic import BaseModel, Field

class ClientCreate(BaseModel):
    kdnr: str = Field(..., min_length=1)
    name: str

class ClientRead(ClientCreate):
    id: str
