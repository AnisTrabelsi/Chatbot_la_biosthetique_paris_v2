from celery import Celery
from app.services.portatour_service import collect_client_data
from app.services.llm_service import enrich_visit_prompt
from app.services.invoice_service import build_docx
from app.services.pdf_service import convert_to_pdf
from app.db.session import AsyncSessionLocal
from app.core.ws_manager import manager
import asyncio

celery_app = Celery("prep_tasks")
celery_app.config_from_object("app.core.config", namespace="CELERY_")

import asyncio

@celery_app.task(name="prep_visit_task")
def prep_visit_task(prep_id: str, user_id: str, client_id: str):
    async def _run():
        async with AsyncSessionLocal() as db:
            # … collect, enrich, build_docx, convert_to_pdf …
            pdf_path = convert_to_pdf(docx_path)
            await manager.notify_prep_ready(user_id, prep_id, pdf_path)

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # pas de loop actif → safe to use asyncio.run()
        asyncio.run(_run())
    else:
        # loop actif (tests) → schedule and wait
        fut = asyncio.run_coroutine_threadsafe(_run(), loop)
        fut.result()
