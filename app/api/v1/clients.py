from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select

from app.db.session import get_db
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientRead, ClientUpdate

router = APIRouter(prefix="/v1/clients", tags=["clients"])

async def _get_current_user_id(x_user_id: str = Header(..., alias="X-User-ID")) -> str:
    return x_user_id

@router.post("", response_model=ClientRead, status_code=201)
async def create_client(
    payload: ClientCreate,
    user_id: str = Depends(_get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Créer un nouveau client."""
    client = Client(**payload.model_dump(by_alias=True))
    client.owner_id = user_id
    db.add(client)
    await db.commit()
    await db.refresh(client)
    return client

@router.get("", response_model=List[ClientRead])
async def list_clients(
    user_id: str = Depends(_get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Lister tous les clients du commercial."""
    q = await db.execute(
        select(Client).where(Client.owner_id == user_id)
    )
    return q.scalars().all()

@router.get("/{client_id}", response_model=ClientRead)
async def get_client(
    client_id: str,
    user_id: str = Depends(_get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Récupérer un client par ID."""
    client = await db.get(Client, client_id)
    if not client or client.owner_id != user_id:
        raise HTTPException(404, "Client non trouvé")
    return client

@router.patch("/{client_id}", response_model=ClientRead)
async def update_client(
    client_id: str,
    payload: ClientUpdate,
    user_id: str = Depends(_get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Mettre à jour un client."""
    client = await db.get(Client, client_id)
    if not client or client.owner_id != user_id:
        raise HTTPException(404, "Client non trouvé")
    update_data = payload.model_dump(exclude_none=True, by_alias=True)
    for field, val in update_data.items():
        setattr(client, field, val)
    await db.commit()
    await db.refresh(client)
    return client

@router.delete("/{client_id}", status_code=204)
async def delete_client(
    client_id: str,
    user_id: str = Depends(_get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Supprimer un client."""
    client = await db.get(Client, client_id)
    if not client or client.owner_id != user_id:
        raise HTTPException(404, "Client non trouvé")
    await db.delete(client)
    await db.commit()
    return
