# tests/test_tasks_llm.py
import pytest
from app.tasks.llm import prep_visit_task
from app.services.portatour_service import collect_client_data
from app.services.llm_service import enrich_visit_prompt
from app.services.invo_ce_service import build_docx
from app.services.pdf_service import convert_to_pdf

@pytest.mark.asyncio
async def test_prep_visit_task(monkeypatch, tmp_path):
    # Stubs pour chaque étape
    monkeypatch.setattr(
        "app.services.portatour_service.collect_client_data",
        lambda db, client_id: {"name":"X","kdnr":"K1"}
    )
    monkeypatch.setattr(
        "app.services.llm_service.enrich_visit_prompt",
        lambda data: "prompt"
    )
    made = {}
    def fake_build(prep_id, data, prompt):
        p = tmp_path / f"{prep_id}.docx"
        p.write_text("doc")
        made['docx'] = str(p)
        return str(p)
    monkeypatch.setattr(
        "app.services.invo_ce_service.build_docx",
        fake_build
    )
    def fake_convert(docx):
        p = tmp_path / f"{Path(docx).stem}.pdf"
        p.write_text("pdf")
        made['pdf'] = str(p)
        return str(p)
    monkeypatch.setattr(
        "app.services.pdf_service.convert_to_pdf",
        fake_convert
    )

    # Exécute la task synchronously
    result = prep_visit_task.run("P1", "U1", "C1")
    assert 'docx' in made and 'pdf' in made
