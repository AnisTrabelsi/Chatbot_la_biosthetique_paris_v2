# tests/test_schemas.py
import pytest
from pydantic import ValidationError
from app.schemas.client import ClientCreate

def test_client_requires_kdnr():
    with pytest.raises(ValidationError):
        ClientCreate(name="Alice")

def test_kdnr_min_len():
    with pytest.raises(ValidationError):
        ClientCreate(kdnr="", name="Bob")
