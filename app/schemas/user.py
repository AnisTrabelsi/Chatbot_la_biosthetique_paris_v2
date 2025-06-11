# app/schemas/user.py
from __future__ import annotations

# ─── typing helpers ────────────────────────────────────────────
from typing import Annotated

from pydantic import BaseModel, Field, confloat

# --------- READ ---------
class UserRead(BaseModel):
    id: str
    latitude: float | None = None
    longitude: float | None = None
    sector: str | None = None
    onboarded: bool

    model_config = {"from_attributes": True}


# --------- UPDATE ----------
class UserUpdateLocation(BaseModel):
    latitude: Annotated[float, confloat(ge=-90, le=90)] = Field(..., example=48.8566)
    longitude: Annotated[float, confloat(ge=-180, le=180)] = Field(..., example=2.3522)


class UserUpdateSector(BaseModel):
    sector: str = Field(..., min_length=1, max_length=120, example="Paris-Ouest")

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

class LocationUpdate(BaseModel):
    latitude: confloat(ge=-90, le=90)  = Field(..., example=48.8566)
    longitude: confloat(ge=-180, le=180) = Field(..., example=2.3522)

class SectorUpdate(BaseModel):
    sector: str = Field(..., min_length=1, max_length=120, example="Paris-Ouest")    