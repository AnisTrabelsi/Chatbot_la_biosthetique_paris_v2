from fastapi import APIRouter, UploadFile, File, Header, HTTPException, Depends
from minio import Minio
from uuid import uuid4
import io
from app.schemas.catalog import CatalogPDFRead
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.tasks.catalog import parse_pdf_task
from app.models.catalog_pdf import CatalogPDF

router = APIRouter(prefix="/v1/catalog", tags=["catalog"])

# Initialisation du client MinIO (à configurer en prod via app.core.config)
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
    # Validation du type de fichier
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF allowed")

    # Génération d'un ID unique et version
    base_id = uuid4().hex
    version = 1  # à ajuster si versioning en base
    object_name = f"catalog/{base_id}_v{version}.pdf"

    # Lecture du contenu
    content = await file.read()

    # Upload vers MinIO
    minio_client.put_object(
        bucket_name="uploads",
        object_name=object_name,
        data=io.BytesIO(content),
        length=len(content),
        content_type="application/pdf"
    )

    # Lancement asynchrone de la tâche de parsing
    parse_pdf_task.delay(object_name, doc_type, file.filename, version)

    # Création immédiate de l'instance (metadata vide)
    cp = CatalogPDF(
        id=base_id,
        doc_type=doc_type,
        filename=file.filename,
        version=version,
        meta={}  # champ JSON dans le modèle
    )
    db.add(cp)
    await db.commit()
    await db.refresh(cp)
    return cp
