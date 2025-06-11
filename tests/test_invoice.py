# tests/test_invoices.py
import pytest
from io import BytesIO
from httpx import AsyncClient, ASGITransport
from main import app

PDF_BYTES = b"%PDF-1.4 fake pdf"

@pytest.mark.asyncio
async def test_upload_invoice(monkeypatch):
    called = {}
    monkeypatch.setattr(
        "app.tasks.invoice.parse_invoice_pdf_task.delay",
        lambda invoice_id, path: called.setdefault("args", (invoice_id, path))
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        files = {"file": ("inv.pdf", BytesIO(PDF_BYTES), "application/pdf")}
        data = {"client_id": "C123"}
        resp = await ac.post(
            "/v1/invoices",
            headers={"X-User-ID": "user1"},
            files=files,
            data=data,
        )

    assert resp.status_code == 200
    json = resp.json()
    assert json["client_id"] == "C123"
    assert json["filename"] == "inv.pdf"
    invoice_id = json["id"]
    assert called["args"][0] == invoice_id

@pytest.mark.asyncio
async def test_get_invoice_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get(
            "/v1/invoices/nonexistent",
            headers={"X-User-ID": "user1"}
        )
    assert resp.status_code == 404
