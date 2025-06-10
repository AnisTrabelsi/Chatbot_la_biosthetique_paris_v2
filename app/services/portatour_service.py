from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.client import Client

async def collect_client_data(db: AsyncSession, client_id: str) -> dict:
    """
    Récupère les informations du client depuis la base de données.
    Retourne un dictionnaire minimal pour le pipeline de préparation de visite.
    """
    result = await db.execute(select(Client).where(Client.id == client_id))
    client = result.scalar_one_or_none()
    if not client:
        raise ValueError(f"Client with id {client_id} not found")
    return {
        "client_id": client.id,
        "kdnr": client.kdnr,
        "name": client.name,
    }
