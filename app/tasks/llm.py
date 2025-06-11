from __future__ import annotations

import asyncio
from celery import Celery
from sqlalchemy import select

# import de services (pour que le monkey-patching fonctionne en tests)
from app.services import portatour_service, llm_service, prep_service, pdf_service
from app.services.whatsapp_service import send_document
from app.core.ws_manager import manager
from app.db.session import AsyncSessionLocal          # ✅ usine de sessions
from app.models.session import WASession
from celery.signals import after_setup_task_logger
celery_app = Celery("prep_tasks")
celery_app.config_from_object("app.core.config", namespace="CELERY_")

celery_app.conf.task_always_eager = True
@celery_app.task(name="prep_visit_task")
def prep_visit_task(prep_id: str, user_id: str, client_id: str) -> None:
    """
    Pipeline complet de préparation de visite :
    collecte → LLM → DOCX → PDF → notifications.

    En mode *eager* (tests) on saute toute I/O base ou réseau inutile.
    """

    async def _run() -> None:
        # ── 1. collecte des données Portatour ───────────────────────────
        if celery_app.conf.task_always_eager:
            data = await portatour_service.collect_client_data(None, client_id)
        else:
            async with AsyncSessionLocal() as db:
                data = await portatour_service.collect_client_data(db, client_id)

        # ── 2. génération/enrichissement du prompt LLM ──────────────────
        prompt = await llm_service.enrich_visit_prompt(data)

        # ── 3. construction DOCX puis conversion PDF ────────────────────
        docx_path = prep_service.build_docx(prep_id, data, prompt)
        pdf_path = pdf_service.convert_to_pdf(docx_path)

        # ── 4. notification web-socket front ────────────────────────────
        await manager.notify_prep_ready(user_id, prep_id, pdf_path)

        # ── 5. notification WhatsApp (hors tests) ───────────────────────
        if not celery_app.conf.task_always_eager:
            async with AsyncSessionLocal() as db:
                res = await db.execute(
                    select(WASession).where(WASession.user_id == user_id)
                )
                wa = res.scalar_one_or_none()
                if wa:
                    # import « paresseux » pour éviter la dépendance en tests
                    from app.services.minio_service import sign_minio_url

                    pdf_url = sign_minio_url(pdf_path)
                    await send_document(
                        wa.phone_number, pdf_url, f"prep_{client_id}.pdf"
                    )

    asyncio.run(_run())
