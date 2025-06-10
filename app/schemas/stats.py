# app/schemas/stats.py
from pydantic import BaseModel
from datetime import datetime
from typing import Any

class StatsFileCreate(BaseModel):
    kdnr: str
    data: dict[str, Any]

class StatsFileRead(StatsFileCreate):
    id: str
    uploaded_at: datetime
