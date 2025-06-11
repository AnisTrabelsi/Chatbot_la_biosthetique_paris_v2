# tests/test_user_profile.py
import pytest, uuid
from httpx import AsyncClient
from main import app
from fastapi.responses import Response
from fastapi.testclient import TestClient
from tests.conftest import *

@pytest.mark.asyncio
async def test_update_location():
    uid = str(uuid.uuid4())
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # crée user via auth fake
        await ac.post("/v1/auth/portatour", headers={"X-User-ID":uid}, json={"login":"u","password":"p"})
        # maj location
        r = await ac.patch("/v1/users/me/location", headers={"X-User-ID":uid},
                           json={"latitude":48.0,"longitude":2.0})
        assert r.status_code == 200
        data = r.json()
        assert data["latitude"] == 48.0 and data["longitude"] == 2.0
