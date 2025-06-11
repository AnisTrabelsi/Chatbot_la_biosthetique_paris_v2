import uuid
from io import BytesIO

import pandas as pd
import pytest
from httpx import ASGITransport, AsyncClient

from main import app

###############################################################################
# helpers
###############################################################################


@pytest.fixture
def sample_excel_bytes() -> bytes:
    """Génère un classeur Excel minimal (in-memory)."""
    df = pd.DataFrame(
        [
            {"col1": 1, "col2": "A"},
            {"col1": 2, "col2": "B"},
        ]
    )
    buf = BytesIO()
    df.to_excel(buf, index=False)
    return buf.getvalue()


###############################################################################
# tests
###############################################################################


@pytest.mark.asyncio
async def test_upload_stats(sample_excel_bytes):
    """
    Cas nominal :
    1. On crée d’abord le client via l’API /v1/clients
    2. On uploade un fichier Excel pour ce client
    """
    kdnr = "K100"
    user_id = "user1"

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # ► 1. création du client (prérequis de l’endpoint stats)
        create_resp = await ac.post(
            "/v1/clients",
            headers={"X-User-ID": user_id},
            json={
                "kdnr": kdnr,
                "name": "ACME",
                "phone": "+33123456789",
            },
        )
        assert create_resp.status_code == 201

        # ► 2. upload Excel
        files = {
            "file": (
                "test.xlsx",
                sample_excel_bytes,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        }
        resp = await ac.post(
            "/v1/stats/upload",
            headers={"X-User-ID": user_id},
            data={"kdnr": kdnr},
            files=files,
        )

    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list) and len(data) == 2
    assert all(item["kdnr"] == kdnr for item in data)


@pytest.mark.asyncio
async def test_upload_stats_unknown_client(sample_excel_bytes):
    """Si le client n'existe pas, l'API renvoie 404."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        files = {
            "file": (
                "test.xlsx",
                sample_excel_bytes,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        }
        resp = await ac.post(
            "/v1/stats/upload",
            headers={"X-User-ID": "user1"},
            data={"kdnr": "NOPE999"},
            files=files,
        )

    assert resp.status_code == 404
