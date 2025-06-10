# app/schemas/user.py
from pydantic import BaseModel

class UserRead(BaseModel):
    id: str
    latitude: float | None
    longitude: float | None
    sector: str | None
    onboarded: bool

    class Config:
        orm_mode = True
