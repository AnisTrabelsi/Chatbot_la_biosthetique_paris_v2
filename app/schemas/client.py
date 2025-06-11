from __future__ import annotations

import phonenumbers
from pydantic import BaseModel, Field, ConfigDict, constr, field_validator

# ───────── helpers ────────────────────────────────────────────────────────────
def _normalize_phone(value: str) -> str:
    """Valide & normalise en E.164 (+33…)."""
    try:
        num = phonenumbers.parse(value, None)
        if not phonenumbers.is_valid_number(num):
            raise ValueError
        return phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.E164)
    except Exception:
        raise ValueError("phone must be valid E.164 like +33612345678")

def _luhn_ok(number: str) -> bool:
    total, alt = 0, False
    for digit in reversed(number):
        d = int(digit)
        if alt:
            d = d * 2 - 9 if d * 2 > 9 else d * 2
        total += d
        alt = not alt
    return total % 10 == 0

# ───────── Base schema ────────────────────────────────────────────────────────
class ClientBase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,  # accepte phone= dans l’input
        from_attributes=True,   # ORM <-> Pydantic
    )

    name: constr(min_length=2, max_length=100)
    # alias JSON = "phone" pour coller aux tests
    phone_e164: str = Field(..., alias="phone", examples=["+33612345678"])
    kdnr: constr(pattern=r"^\d{3,8}$") | None = Field(
        default=None, description="Numéro client (3-8 chiffres)"
    )
    siret: constr(pattern=r"^\d{14}$") | None = Field(
        default=None, description="SIRET 14 chiffres"
    )

    # ▶︎  validate phone
    @field_validator("phone_e164")
    @classmethod
    def _validate_phone(cls, v: str) -> str:
        return _normalize_phone(v)

    # ▶︎  validate SIRET checksum (Luhn)
    @field_validator("siret")
    @classmethod
    def _validate_siret(cls, v: str | None) -> str | None:
        if v and not _luhn_ok(v):
            raise ValueError("invalid SIRET (checksum)")
        return v

    # --- alias d'accès (.phone) pour rester compatible avec les tests -------
    @property
    def phone(self) -> str:
        """Alias lecture : retourne le numéro en E.164."""
        return self.phone_e164

# ───────── CRUD schemas ───────────────────────────────────────────────────────
class ClientCreate(ClientBase):
    """Schema utilisé lors de la création."""


class ClientRead(ClientBase):
    id: str
