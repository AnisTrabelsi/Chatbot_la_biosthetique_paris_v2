# app/schemas/user.py
from pydantic import BaseModel, Field
from typing import Optional

# ── READ ────────────────────────────────────────────────────────────────
class UserRead(BaseModel):
    id: str
    latitude: Optional[float]
    longitude: Optional[float]
    sector: Optional[str]
    onboarded: bool

    class Config:
        from_attributes = True


# ── WRITE / UPDATE ──────────────────────────────────────────────────────
class UserUpdateLocation(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class UserUpdateSector(BaseModel):
    sector: str = Field(..., min_length=1, max_length=100)


# ── AUTH PORTATOUR ──────────────────────────────────────────────────────
class PortatourAuthIn(BaseModel):
    """Requête d’auth vers Portatour (login / password ou API-Key)."""
    login: str = Field(..., example="user@example.com")
    password: str = Field(..., example="secret123")


# ▸ Alias exigés par les anciens tests / import : -----------------------
AuthPortatourRequest = PortatourAuthIn
class AuthPortatourResponse(UserRead):  # même payload que UserRead
    pass


class AuthPortatourResponse(BaseModel):
    """Réponse du POST /auth/portatour – renvoie un jeton simulé."""
    access_token: str = Field(..., example="pt_alice_token")
    token_type: str = Field(default="bearer", example="bearer")