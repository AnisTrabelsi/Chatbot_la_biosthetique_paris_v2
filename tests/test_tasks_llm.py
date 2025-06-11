import os
from pathlib import Path

import pytest

from app.tasks.llm import prep_visit_task


# ── exécution Celery en mode eager pour chaque test ─────────────────────────
@pytest.fixture(autouse=True)
def eager_celery():
    os.environ["CELERY_EAGER"] = "1"
    yield
    os.environ["CELERY_EAGER"] = "0"


def test_prep_visit_task(monkeypatch, tmp_path):
    # ► Stubs
    async def fake_collect(db, cid):
        return {"name": "X", "kdnr": "K1"}

    async def fake_enrich(data):
        return "prompt-text"

    def fake_build(prep_id, data, prompt):
        p = tmp_path / f"{prep_id}.docx"
        p.write_text("docx")
        return str(p)

    def fake_convert(docx_path):
        p = tmp_path / f"{Path(docx_path).stem}.pdf"
        p.write_text("pdf")
        return str(p)

    monkeypatch.setattr(
        "app.services.portatour_service.collect_client_data", fake_collect
    )
    monkeypatch.setattr("app.services.llm_service.enrich_visit_prompt", fake_enrich)
    monkeypatch.setattr("app.services.prep_service.build_docx", fake_build)
    monkeypatch.setattr("app.services.pdf_service.convert_to_pdf", fake_convert)

    # ► run
    prep_visit_task("P1", "U1", "C1")

    assert (tmp_path / "P1.docx").exists()
    assert (tmp_path / "P1.pdf").exists()
