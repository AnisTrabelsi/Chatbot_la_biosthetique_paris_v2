import pytest
from pydantic import ValidationError
from app.schemas.client import ClientCreate
from app.schemas.stats import StatsFileCreate

def test_client_requires_kdnr():
    with pytest.raises(ValidationError):
        ClientCreate(name="Alice")

def test_client_phone_e164():
    # mauvais format => ValidationError
    with pytest.raises(ValidationError):
        ClientCreate(kdnr="123", name="Bob", phone="0609123456")
    # bon format
    ok = ClientCreate(kdnr="123", name="Bob", phone="+33609123456")
    assert ok.phone == "+33609123456"

def test_statsfile_data_must_be_dict():
    with pytest.raises(ValidationError):
        StatsFileCreate(kdnr="123", data="not a dict")
