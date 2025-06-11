from celery import Celery
from app.services.catalog_service import parse_pdf_metadata
from app.db.session import AsyncSessionLocal
from app.models.catalog_pdf import CatalogPDF

celery_app = Celery("catalog_tasks")
celery_app.config_from_object("app.core.config", namespace="CELERY_")

@celery_app.task(name="parse_pdf_task")
def parse_pdf_task(file_path: str, doc_type: str, filename: str, version: int):
    import asyncio, io
    from sqlalchemy.ext.asyncio import AsyncSession

    async def _run():
        # lire les bytes
        b = open(file_path, "rb").read()
        metadata = await parse_pdf_metadata(b)
        async with AsyncSessionLocal() as db:
            cp = CatalogPDF(
                doc_type=doc_type,
                filename=filename,
                version=version,
                metadata=metadata
            )
            db.add(cp)
            await db.commit()

    asyncio.run(_run())
