from pydantic import BaseModel
from datetime import datetime
from typing import Any, Dict

class StatsFileCreate(BaseModel):
    kdnr: str
    data: Dict[str, Any]

class StatsFileRead(StatsFileCreate):
    id: str
    uploaded_at: datetime

    class Config:
        orm_mode = True
