from celery import Celery
from app.services.excel_service import parse_stats_excel
from app.db.session import AsyncSessionLocal

celery_app = Celery("stats_tasks")
celery_app.config_from_object("app.core.config", namespace="CELERY_")

@celery_app.task(name="parse_stats_excel_task")
def parse_stats_excel_task(file_path: str, kdnr: str):
    """
    Lit le fichier depuis `file_path`, puis invoque parse_stats_excel
    dans un contexte AsyncSessionLocal.
    """
    # lire le fichier en binaire
    with open(file_path, "rb") as f:
        file_bytes = f.read()

    async def _run():
        async with AsyncSessionLocal() as db:
            await parse_stats_excel(file_bytes, kdnr, db)

    import asyncio
    asyncio.run(_run())
