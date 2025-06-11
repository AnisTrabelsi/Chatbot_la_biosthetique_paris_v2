from celery import Celery
from app.services.catalog_service import parse_pdf_metadata
from app.db.session import AsyncSessionLocal
from app.models.catalog_pdf import CatalogPDF
import asyncio

celery_app = Celery("catalog_tasks")
celery_app.config_from_object("app.core.config", namespace="CELERY_")

@celery_app.task(name="parse_pdf_task")
def parse_pdf_task(file_path: str, doc_type: str, filename: str, version: int):
    """
    Tâche Celery qui lit le fichier PDF, en extrait les metadata,
    puis crée un enregistrement CatalogPDF dans la base.
    """
    async def _run():
        # 1. Lecture des bytes
        with open(file_path, "rb") as f:
            b = f.read()

        # 2. Extraction metadata
        metadata = await parse_pdf_metadata(b)

        # 3. Insertion en BDD
        async with AsyncSessionLocal() as db:
            cp = CatalogPDF(
                doc_type=doc_type,
                filename=filename,
                version=version,
                meta=metadata,  # correspond à la colonne JSON "metadata"
            )
            db.add(cp)
            await db.commit()

    # Exécution de la coroutine dans un nouvel event loop
    asyncio.run(_run())
