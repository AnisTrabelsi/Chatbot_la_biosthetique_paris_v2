import pytest
from pathlib import Path
from app.tasks.llm import prep_visit_task
from app.services.portatour_service import collect_client_data
from app.services.llm_service import enrich_visit_prompt
from app.services.invoice_service import build_docx
from app.services.pdf_service import convert_to_pdf

@pytest.fixture(autouse=True)
def configure_celery_eager(monkeypatch):
    from app.tasks.llm import celery_app
    celery_app.conf.task_always_eager = True
    celery_app.conf.task_eager_propagates = True

@pytest.mark.asyncio
async def test_prep_visit_task(monkeypatch, tmp_path):
    # Stub collect_client_data
    async def fake_collect(db, cid):
        return {"name": "X", "kdnr": "K1"}
    monkeypatch.setattr(
        "app.services.portatour_service.collect_client_data",
        fake_collect
    )
    # Stub enrich_visit_prompt
    async def fake_enrich(data):
        return "prompt-text"
    monkeypatch.setattr(
        "app.services.llm_service.enrich_visit_prompt",
        fake_enrich
    )
    # Stub build_docx
    def fake_build(prep_id, data, prompt):
        p = tmp_path / f"{prep_id}.docx"
        p.write_text("docx")
        return str(p)
    monkeypatch.setattr(
        "app.services.invoice_service.build_docx",
        fake_build
    )
    # Stub convert_to_pdf
    def fake_convert(docx):
        p = tmp_path / f"{Path(docx).stem}.pdf"
        p.write_text("pdf")
        return str(p)
    monkeypatch.setattr(
        "app.services.pdf_service.convert_to_pdf",
        fake_convert
    )

    # Execute synchronously
    prep_visit_task("P1", "U1", "C1")

    # Verify files created
    assert (tmp_path / "P1.docx").exists()
    assert (tmp_path / "P1.pdf").exists()
