from pydantic import BaseModel, Field
from datetime import datetime


class InvoiceRead(BaseModel):
    id: str
    client_id: str
    filename: str
    file_path: str
    uploaded_at: datetime
    meta: dict = Field(..., alias="meta")

    model_config = {"from_attributes": True, "populate_by_name": True}
