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

@celery_app.task(name="prep_visit_task")
def prep_visit_task(prep_id: str, user_id: str, client_id: str):
    async def _run():
        async with AsyncSessionLocal() as db:
            # 1. Récupération des données client
            client_data = await collect_client_data(db, client_id)
            # 2. Génération du prompt via LLM
            prompt = await enrich_visit_prompt(client_data)
            # 3. Génération du DOCX
            docx_path = build_docx(prep_id, client_data, prompt)
            # 4. Conversion en PDF
            pdf_path = convert_to_pdf(docx_path)
            # 5. Notification via WebSocket
            await manager.notify_prep_ready(user_id, prep_id, pdf_path)

    # Exécution de la coroutine
    asyncio.run(_run())
