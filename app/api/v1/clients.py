from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientRead

router = APIRouter(prefix="/v1/clients", tags=["clients"])

@router.post("", response_model=ClientRead)
async def create_client(
    body: ClientCreate,
    x_user_id: str = Header(..., alias="X-User-ID"),
    db: AsyncSession = Depends(get_db),
):
    # vérif doublon kdnr
    existing = await db.execute(
        Client.__table__.select().where(Client.kdnr == body.kdnr)
    )
    if existing.scalar():
        raise HTTPException(409, "Kdnr already exists")

    client = Client(**body.dict())
    db.add(client)
    await db.commit()
    await db.refresh(client)
    return client
