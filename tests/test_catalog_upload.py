import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from io import BytesIO

PDF_BYTES = b"%PDF-1.4 fake pdf"

@pytest.mark.asyncio
async def test_catalog_upload():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        files = {
            "file": (
                "offer.pdf",
                BytesIO(PDF_BYTES),
                "application/pdf"
            )
        }
        params = {"doc_type": "offer"}
        resp = await ac.post(
            "/v1/catalog/upload",
            headers={"X-User-ID": "u1"},
            params=params,
            files=files,
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["doc_type"] == "offer"
    assert data["filename"] == "offer.pdf"
    assert data["metadata"] == {}  # parsing asynchrone pas encore appliqué
