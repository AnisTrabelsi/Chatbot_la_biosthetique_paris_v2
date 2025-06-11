# app/services/excel_service.py
import uuid
import pandas as pd
from io import BytesIO
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.client import Client
from app.models.stats_file import StatsFile

async def parse_stats_excel(content: bytes, kdnr: str, db: AsyncSession) -> list[StatsFile]:
    """
    • Vérifie que le client existe (kdnr = 1 lettre optionnelle + 3-8 digits).
    • Parse le classeur excel (stub minimal pour les tests).
    • Crée un StatsFile par ligne et les persiste.
    """
    # ── 1. client must exist ────────────────────────────────────────────────
    res = await db.execute(select(Client).where(Client.kdnr == kdnr))
    client = res.scalar_one_or_none()
    if client is None:
        raise HTTPException(404, "Client not found")

    # ── 2. parse excel (very light) ────────────────────────────────────────
    df = pd.read_excel(BytesIO(content))

    stats_objs: list[StatsFile] = []
    for _, row in df.iterrows():
        stats = StatsFile(
            id=str(uuid.uuid4()),
            kdnr=kdnr,
            raw=row.to_json(),          # on stocke brut pour le stub
        )
        db.add(stats)
        stats_objs.append(stats)

    await db.commit()
    return stats_objs
