from pydantic import BaseModel
from datetime import datetime

class WASessionRead(BaseModel):
    id: str
    phone_number: str
    created_at: datetime
    is_closed: bool

    model_config = {"from_attributes": True}

class LeadEnrichmentRead(BaseModel):
    id: str
    session_id: str
    data: dict
    score: str
    created_at: datetime

    model_config = {"from_attributes": True}

class ProspectNotification(BaseModel):
    session: WASessionRead
    enrichment: LeadEnrichmentRead
