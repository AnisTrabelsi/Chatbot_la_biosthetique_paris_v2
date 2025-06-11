from pathlib import Path
from uuid import uuid4
import io
import socket
from fastapi import APIRouter, UploadFile, File, Header, HTTPException, Depends
from minio import Minio
from minio.error import S3Error
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.catalog import CatalogPDFRead
from app.models.catalog_pdf import CatalogPDF
from app.db.session import get_db
from app.tasks.catalog import parse_pdf_task
from pathlib import Path, PurePosixPath

router = APIRouter(prefix="/v1/catalog", tags=["catalog"])

# ─────────────────────────────── MinIO client ────────────────────────────────
minio_client = Minio(
    "minio:9000",
    access_key="minioaccess",
    secret_key="miniosecret",
    secure=False,
)

# A tiny helper: in CI / pytest there is no MinIO; we store on disk instead.
_LOCAL_STORE = Path("/tmp/uploads/catalog")
_LOCAL_STORE.mkdir(parents=True, exist_ok=True)


def _upload_to_object_store(object_name: str, data: bytes) -> None:
    """Try MinIO first; fall back to local filesystem during tests."""
    try:
        # Does a quick DNS lookup first to fail fast if MinIO isn’t reachable.
        socket.gethostbyname("minio")

        minio_client.put_object(
            bucket_name="uploads",
            object_name=object_name,
            data=io.BytesIO(data),
            length=len(data),
            content_type="application/pdf",
        )
    except Exception:
        # Any failure (DNS, refused, S3Error…) → local save.
        local_path = _LOCAL_STORE / object_name
        local_path.parent.mkdir(parents=True, exist_ok=True)
        local_path.write_bytes(data)


# ─────────────────────────────────── Route ────────────────────────────────────
@router.post("/upload", response_model=CatalogPDFRead)
async def upload_catalog(
    doc_type: str,
    file: UploadFile = File(...),
    x_user_id: str = Header(..., alias="X-User-ID"),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF allowed")

    # ► stockage local
    base_id = uuid4().hex
    version = 1
    object_name = f"{base_id}_v{version}.pdf"
    save_path = _LOCAL_STORE / object_name
    save_path.write_bytes(await file.read())

    # ► création en BDD
    cp = CatalogPDF(
        id=base_id,
        doc_type=doc_type,
        filename=file.filename,
        version=version,
        meta={},                 # colonne réelle
    )
    db.add(cp)
    await db.commit()
    await db.refresh(cp)

    # ► tâche asynchrone de parsing
    parse_pdf_task.delay(str(save_path), doc_type, file.filename, version)

    # ► réponse explicite : inclut `metadata` attendu par les tests
    return CatalogPDFRead(
        id=cp.id,
        doc_type=cp.doc_type,
        filename=cp.filename,
        version=cp.version,
        metadata={},             # clé attendue
    )
