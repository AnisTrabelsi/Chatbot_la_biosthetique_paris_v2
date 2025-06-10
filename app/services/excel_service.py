import pandas as pd
from io import BytesIO
from typing import List, Dict
from app.models.stats_file import StatsFile
from sqlalchemy.ext.asyncio import AsyncSession

async def parse_stats_excel(
    file_bytes: bytes, kdnr: str, db: AsyncSession
) -> List[StatsFile]:
    """
    Lit un Excel (bytes), extrait chaque feuille (ou la première),
    transforme en JSON ligne par ligne, stocke en DB.
    Retourne la liste des StatsFile créés.
    """
    # Charger avec pandas
    df = pd.read_excel(BytesIO(file_bytes), sheet_name=0)
    results = []
    for idx, row in df.iterrows():
        data = row.to_dict()
        stats = StatsFile(kdnr=kdnr, data=data)
        db.add(stats)
        results.append(stats)
    await db.commit()
    # Rafraîchir pour avoir les IDs
    for stats in results:
        await db.refresh(stats)
    return results
