import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_missing_header():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/v1/auth/portatour", json={"login":"a","password":"b"})
    assert resp.status_code == 401

@pytest.mark.asyncio
async def test_auth_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(
            "/v1/auth/portatour",
            headers={"X-User-ID":"u123"},
            json={"login":"alice","password":"pwd"}
        )
    assert resp.status_code == 200
    assert "access_token" in resp.json()
