from fastapi import APIRouter, UploadFile, File, Header, HTTPException, Depends
from minio import Minio
from uuid import uuid4
from app.schemas.catalog import CatalogPDFRead
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.tasks.catalog import parse_pdf_task

router = APIRouter(prefix="/v1/catalog", tags=["catalog"])

# Init MinIO client (depuis config)
minio_client = Minio(
    "minio:9000",
    access_key="minioaccess",
    secret_key="miniosecret",
    secure=False
)

@router.post("/upload", response_model=CatalogPDFRead)
async def upload_catalog(
    doc_type: str,
    file: UploadFile = File(...),
    x_user_id: str = Header(..., alias="X-User-ID"),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF allowed")
    # Générer un nom unique et version
    base_id = uuid4().hex
    version = 1  # ou calculer depuis la DB
    object_name = f"catalog/{base_id}_v{version}.pdf"
    # Uploader dans MinIO
    content = await file.read()
    minio_client.put_object(
        bucket_name="uploads",
        object_name=object_name,
        data=io.BytesIO(content),
        length=len(content),
        content_type="application/pdf"
    )
    # Lancer la tâche de parsing
    parse_pdf_task.delay(object_name, doc_type, file.filename, version)
    # Créer l’instance vide à retourner (metadata sera mis à jour plus tard)
    from app.models.catalog_pdf import CatalogPDF
    cp = CatalogPDF(
        id=base_id,
        doc_type=doc_type,
        filename=file.filename,
        version=version,
        metadata={}
    )
    db.add(cp)
    await db.commit()
    await db.refresh(cp)
    return cp
