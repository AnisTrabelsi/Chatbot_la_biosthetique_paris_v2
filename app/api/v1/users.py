# app/api/v1/users.py
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import (
    UserRead,
    UserUpdateLocation,
    UserUpdateSector,
)

router = APIRouter(prefix="/users", tags=["users"])

async def _get_current_user(
    x_user_id: str = Header(..., alias="X-User-ID"),
    db: AsyncSession = Depends(get_db),
) -> User:
    user = await db.get(User, x_user_id)
    if not user:
        raise HTTPException(404, "Utilisateur non trouvé")
    return user

@router.get("/me", response_model=UserRead)
async def read_profile(user: User = Depends(_get_current_user)):
    """Retourne le profil du commercial."""
    return user

@router.patch("/me/location", response_model=UserRead)
async def update_location(
    coords: UserUpdateLocation,
    user: User = Depends(_get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Met à jour la position GPS."""
    user.latitude = coords.latitude
    user.longitude = coords.longitude
    # si secteur déjà défini → onboarding complet
    if user.sector:
        user.onboarded = True
    await db.commit()
    await db.refresh(user)
    return user

@router.patch("/me/sector", response_model=UserRead)
async def update_sector(
    payload: UserUpdateSector,
    user: User = Depends(_get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Met à jour le secteur."""
    user.sector = payload.sector
    # si coords déjà définies → onboarding complet
    if user.latitude is not None and user.longitude is not None:
        user.onboarded = True
    await db.commit()
    await db.refresh(user)
    return user
