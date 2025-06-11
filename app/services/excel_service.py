from __future__ import annotations

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
    • Vérifie que le client existe.
    • Parse le classeur (stub minimal)
    • Crée un StatsFile par ligne.
    """
    # 1. client doit exister
    res = await db.execute(select(Client).where(Client.kdnr == kdnr))
    client = res.scalar_one_or_none()
    if client is None:
        raise HTTPException(404, "Client not found")

    # 2. parse Excel
    df = pd.read_excel(BytesIO(content))

    stats_objects: list[StatsFile] = []
    for _, row in df.iterrows():
        stats = StatsFile(
            id=str(uuid.uuid4()),
            kdnr=kdnr,
            raw=row.to_json(),
        )
        db.add(stats)
        stats_objects.append(stats)

    await db.commit()
    return stats_objects
