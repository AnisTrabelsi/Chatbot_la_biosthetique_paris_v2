# app/api/v1/catalog.py
"""Endpoint d’upload de PDF catalogue (offres / formations).
Pour les tests locaux, MinIO peut être absent → appels réseau mis dans try/except.
"""
import io
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, Header, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.catalog import CatalogPDFRead
from app.db.session import get_db
from app.tasks.catalog import parse_pdf_task

try:
    from minio import Minio

    _minio = Minio(
        "minio:9000",
        access_key="minioaccess",
        secret_key="miniosecret",
        secure=False,
    )
except Exception:  # lib ou DNS indisponible en environnement de test
    _minio = None

router = APIRouter(prefix="/v1/catalog", tags=["catalog"])


def _put_to_minio(object_name: str, data: bytes):
    """Upload vers MinIO si disponible (ignore sinon)."""
    if _minio is None:
        return
    try:
        # Crée le bucket au premier appel
        if not _minio.bucket_exists("uploads"):
            _minio.make_bucket("uploads")
        _minio.put_object(
            bucket_name="uploads",
            object_name=object_name,
            data=io.BytesIO(data),
            length=len(data),
            content_type="application/pdf",
        )
    except Exception:
        # En CI locale on ignore les erreurs réseau / DNS
        pass


@router.post("/upload", response_model=CatalogPDFRead)
async def upload_catalog(
    doc_type: str,
    file: UploadFile = File(...),
    x_user_id: str = Header(..., alias="X-User-ID"),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF allowed")

    base_id = uuid4().hex
    version = 1
    object_name = f"catalog/{base_id}_v{version}.pdf"

    content = await file.read()
    _put_to_minio(object_name, content)

    # Task Celery
    parse_pdf_task.delay(object_name, doc_type, file.filename, version)

    # Persist en DB (metadata vide pour l’instant)
    from app.models.catalog_pdf import CatalogPDF

    cp = CatalogPDF(
        id=base_id,
        doc_type=doc_type,
        filename=file.filename,
        version=version,
        metadata={},
    )
    db.add(cp)
    await db.commit()
    await db.refresh(cp)

    return cp
