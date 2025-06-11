from pydantic import BaseModel
from datetime import datetime

class CatalogPDFCreate(BaseModel):
    doc_type: str  # “offer” ou “training”
    # Pas besoin de body puisque c’est multipart/form-data

class CatalogPDFRead(BaseModel):
    id: str
    doc_type: str
    filename: str
    uploaded_at: datetime
    metadata: dict

    model_config = {"from_attributes": True}
