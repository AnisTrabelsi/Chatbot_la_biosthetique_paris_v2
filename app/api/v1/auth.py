from fastapi import APIRouter, Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import AuthPortatourRequest, AuthPortatourResponse
from app.services.auth_service import authenticate_with_portatour
from app.db.session import get_db
from app.models.user import User

router = APIRouter(prefix="/v1/auth", tags=["auth"])

@router.post("/portatour", response_model=AuthPortatourResponse)
async def auth_portatour(
    body: AuthPortatourRequest,
    x_user_id: str = Header(..., alias="X-User-ID"),
    db: AsyncSession = Depends(get_db),
):
    try:
        token = await authenticate_with_portatour(body.login, body.password)
    except ValueError:
        raise HTTPException(status_code=401, detail="Bad credentials")

    user = await db.get(User, x_user_id)
    if not user:
        user = User(id=x_user_id)
        db.add(user)
    user.portatour_token = token
    await db.commit()
    return {"access_token": token}
