# tests/test_webhook.py
import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_wa_webhook_and_notify(monkeypatch):
    # Stub create_wa_session
    async def fake_create(db, phone):
        from app.models.session import WASession
        return WASession(id="S1", phone_number=phone)
    monkeypatch.setattr(
        "app.services.whatsapp_service.create_wa_session",
        fake_create
    )
    # Stub enrich_lead_task.delay
    calls = {}
    def fake_delay(sid, phone):
        calls["args"] = (sid, phone)
    monkeypatch.setattr(
        "app.tasks.lead.enrich_lead_task.delay",
        fake_delay
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(
            "/v1/webhook/wa",
            headers={"X-User-ID":"U1"},
            json={"from": "+33123456789"},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["session_id"] == "S1"
    assert calls["args"] == ("S1", "+33123456789")
