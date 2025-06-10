from pydantic import BaseModel


# ---------- Lecture ----------
class UserRead(BaseModel):
    id: str
    latitude: float | None = None
    longitude: float | None = None
    sector: str | None = None
    onboarded: bool

    model_config = {"from_attributes": True}   # (Pydantic v2)


# ---------- Auth ----------
class AuthPortatourRequest(BaseModel):
    login: str
    password: str


class AuthPortatourResponse(BaseModel):
    access_token: str
