# app/api/v1/clients.py
from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.client import ClientCreate, ClientRead
from app.models.client import Client
from app.db.session import get_db

router = APIRouter(prefix="/v1/clients", tags=["clients"])

@router.post("", response_model=ClientRead)
async def create_client(
    body: ClientCreate,
    x_user_id: str = Header(..., alias="X-User-ID"),
    db: AsyncSession = Depends(get_db),
):
    client = Client(**body.dict())
    db.add(client)
    await db.commit()
    await db.refresh(client)
    return client
