from celery import Celery
from app.services.lead_service import enrich_lead_data
from app.db.session import AsyncSessionLocal
from app.models.lead_enrichment import LeadEnrichment
from app.core.ws_manager import manager
import asyncio

celery_app = Celery("lead_tasks")
celery_app.config_from_object("app.core.config", namespace="CELERY_")

@celery_app.task(name="enrich_lead_task")
def enrich_lead_task(session_id: str, phone_number: str):
    async def _run():
        data, score = await enrich_lead_data(phone_number)
        async with AsyncSessionLocal() as db:
            enrichment = LeadEnrichment(
                session_id=session_id,
                data=data,
                score=score
            )
            db.add(enrichment)
            await db.commit()
            await db.refresh(enrichment)
        # charger le session
        from app.services.whatsapp_service import create_wa_session
        # stub : récupérer session existante (on suppose qu’on l’a cr��)
        async with AsyncSessionLocal() as db2:
            obj = await db2.get(WASession, session_id)
        # notifier le commercial en WebSocket
        await manager.notify_prospect_ready(obj.phone_number, session_id, enrichment.dict())

    # run in event loop
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        asyncio.run(_run())
    else:
        fut = asyncio.run_coroutine_threadsafe(_run(), loop)
        fut.result()
