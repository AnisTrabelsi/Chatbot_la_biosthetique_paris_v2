# app/schemas/prep.py
from pydantic import BaseModel, Field


# ----------- phase B-3 : hub documents --------------------------------------
class DocsMeta(BaseModel):
    stats: bool = Field(..., description="bilan Excel présent")
    offer_pdf: bool = Field(..., description="catalogue offres présent")
    training_pdf: bool = Field(..., description="catalogue formations présent")
    invoices: bool = Field(..., description="factures présentes")


# ----------- API /prep/full -------------------------------------------------
class PrepFullRequest(BaseModel):
    client_id: str = Field(..., example="c123")


class PrepFullResponse(BaseModel):
    prep_id: str
