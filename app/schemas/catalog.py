from pydantic import BaseModel
from datetime import datetime
from typing import Dict

class CatalogPDFRead(BaseModel):
    id: str
    doc_type: str
    filename: str
    version: int
    uploaded_at: datetime
    meta: Dict  # correspond à l’attribut meta

    model_config = {"from_attributes": True}
