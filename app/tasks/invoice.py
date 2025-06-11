# app/tasks/invoice.py
from celery import Celery
from app.services.invoice_service import parse_invoice_pdf
from app.db.session import AsyncSessionLocal
from app.models.invoice import Invoice
import asyncio

celery_app = Celery("invoice_tasks")
celery_app.config_from_object("app.core.config", namespace="CELERY_")

@celery_app.task(name="parse_invoice_pdf_task")
def parse_invoice_pdf_task(invoice_id: str, file_path: str):
    async def _run():
        with open(file_path, "rb") as f:
            file_bytes = f.read()
        metadata = await parse_invoice_pdf(file_bytes)
        async with AsyncSessionLocal() as db:
            inv = await db.get(Invoice, invoice_id)
            if inv:
                inv.meta = metadata
                await db.commit()

    try:
        asyncio.run(_run())
    except RuntimeError:
        loop = asyncio.get_event_loop()
        fut = asyncio.run_coroutine_threadsafe(_run(), loop)
        fut.result()