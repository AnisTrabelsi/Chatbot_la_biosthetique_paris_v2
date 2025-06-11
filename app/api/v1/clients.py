# app/api/v1/clients.py
from fastapi import APIRouter, Header, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientRead

router = APIRouter(prefix="/v1/clients", tags=["clients"])

async def _get_current_user(
    x_user_id: str = Header(..., alias="X-User-ID"),
    db: AsyncSession = Depends(get_db),
):
    # si besoin de vérifier l’existence de l’utilisateur, sinon on peut omettre
    return x_user_id

@router.post("", response_model=ClientRead, status_code=status.HTTP_201_CREATED)
async def create_client(
    payload: ClientCreate,
    x_user_id: str = Depends(_get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Crée un client.
    On convertit l’alias `phone` → `phone_e164` pour le modèle SQLAlchemy.
    """
    data = payload.model_dump(by_alias=True)  # {'phone': '+33…', 'kdnr':…, 'name':…, 'siret':…}
    # renommer pour correspondre à la colonne SQLA
    if "phone" in data:
        data["phone_e164"] = data.pop("phone")

    client = Client(**data)
    db.add(client)
    await db.commit()
    await db.refresh(client)
    return client
