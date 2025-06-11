import pytest
from pydantic import ValidationError
from app.schemas.client import ClientCreate

def test_client_schema_ok():
    c = ClientCreate(
        name="Boulangerie Dupont",
        phone_e164="+33612345678",
        kdnr="123456",
        siret="73282932000074",  # Luhn OK
    )
    assert c.phone_e164 == "+33612345678"

def test_bad_phone():
    with pytest.raises(ValidationError):
        ClientCreate(name="X", phone_e164="0612345678")  # pas +33

def test_bad_kdnr():
    with pytest.raises(ValidationError):
        ClientCreate(name="X", phone_e164="+33612345678", kdnr="ABC123")

def test_bad_siret_checksum():
    with pytest.raises(ValidationError):
        ClientCreate(name="X", phone_e164="+33612345678", siret="12345678901234")
