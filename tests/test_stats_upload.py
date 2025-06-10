import pytest
from httpx import AsyncClient, ASGITransport
from main import app
import pandas as pd
from io import BytesIO

@pytest.fixture
def sample_excel_bytes():
    df = pd.DataFrame([{"col1": 1, "col2": "A"}, {"col1": 2, "col2": "B"}])
    buf = BytesIO()
    df.to_excel(buf, index=False)
    return buf.getvalue()

@pytest.mark.asyncio
async def test_upload_stats(sample_excel_bytes):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        files = {"file": ("test.xlsx", sample_excel_bytes, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        data = {"kdnr": "K100"}
        resp = await ac.post("/v1/stats/upload", headers={"X-User-ID":"user1"}, files=files, data=data)
    assert resp.status_code == 200
    result = resp.json()
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(item["kdnr"] == "K100" for item in result)
