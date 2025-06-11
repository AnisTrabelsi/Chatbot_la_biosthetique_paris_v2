from __future__ import annotations

import asyncio
from celery import Celery

# import modules -- NOT individual functions -- so monkey-patching works
from app.services import portatour_service, llm_service, prep_service, pdf_service
from app.core.ws_manager import manager
from app.db.session import AsyncSessionLocal

celery_app = Celery("prep_tasks")
celery_app.config_from_object("app.core.config", namespace="CELERY_")

@celery_app.task(name="prep_visit_task")
def prep_visit_task(prep_id: str, user_id: str, client_id: str) -> None:
    """
    Full preparation pipeline: collect → LLM → DOCX → PDF → websocket notify.

    When Celery runs in *eager* mode (tests), we skip any real database work.
    """

    async def _run() -> None:
        # ── 1. collect data ────────────────────────────────────────────────
        if celery_app.conf.task_always_eager:
            data = await portatour_service.collect_client_data(None, client_id)
        else:
            async with AsyncSessionLocal() as db:
                data = await portatour_service.collect_client_data(db, client_id)

        # ── 2. enrich prompt ───────────────────────────────────────────────
        prompt = await llm_service.enrich_visit_prompt(data)

        # ── 3. build DOCX + PDF ────────────────────────────────────────────
        docx_path = prep_service.build_docx(prep_id, data, prompt)
        pdf_path = pdf_service.convert_to_pdf(docx_path)

        # ── 4. real-time notification ─────────────────────────────────────
        await manager.notify_prep_ready(user_id, prep_id, pdf_path)

    asyncio.run(_run())
