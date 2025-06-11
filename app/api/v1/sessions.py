from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.client import Client
from app.schemas.client import ClientRead

router = APIRouter(prefix="/v1/sessions", tags=["sessions"])

@router.get("/{key}", response_model=ClientRead)
async def get_client_session(
    key: str,
    x_user_id: str = Header(..., alias="X-User-ID"),
    db: AsyncSession = Depends(get_db),
):
    """
    Recherche un client soit par phone_e164, soit par kdnr (si key est numérique).
    Fallback unique Postgres pour l'instant.
    """
    # 1) Recherche par téléphone E.164
    stmt = select(Client).where(Client.phone_e164 == key)
    result = await db.execute(stmt)
    client = result.scalars().first()

    # 2) Si non trouvé et key est numérique → recherche par kdnr
    if not client and key.isdigit():
        stmt = select(Client).where(Client.kdnr == key)
        result = await db.execute(stmt)
        client = result.scalars().first()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client
