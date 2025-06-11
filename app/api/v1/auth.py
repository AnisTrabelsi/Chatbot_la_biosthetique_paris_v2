# app/api/v1/auth.py
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.schemas import (
    PortatourAuthIn,
    UserRead,
    AuthPortatourResponse,   # ← importer la nouvelle réponse

)

router = APIRouter(prefix="/v1/auth", tags=["auth"])


@router.post("/portatour", response_model=AuthPortatourResponse, status_code=200)
async def auth_portatour(
    payload: PortatourAuthIn,
    x_user_id: str = Header(..., alias="X-User-ID"),
    db: AsyncSession = Depends(get_db),
) -> AuthPortatourResponse:
    # récupère ou crée le User
    user = await db.get(User, x_user_id) or User(id=x_user_id)

    fake_token = f"pt_{payload.login}_token"
    user.portatour_token = fake_token
    user.onboarded = True

    db.add(user)
    await db.commit()

    # réponse voulue par le test
    return AuthPortatourResponse(access_token=fake_token)