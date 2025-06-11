from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.schemas import UserRead, UserUpdateLocation, UserUpdateSector

router = APIRouter(prefix="/v1/users", tags=["users"])


# ──────────────────────────────────────────────────────────────
async def _get_current_user(
    x_user_id: str = Header(..., alias="X-User-ID"),
    db: AsyncSession = Depends(get_db),
) -> User:
    user = await db.get(User, x_user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user


# ──────────────────────────────────────────────────────────────
@router.get("/me", response_model=UserRead)
async def read_profile(user: User = Depends(_get_current_user)) -> User:
    """Profil complet du commercial."""
    return user


@router.patch("/me/location", response_model=UserRead)
async def update_location(
    coords: UserUpdateLocation,
    user: User = Depends(_get_current_user),
    db: AsyncSession = Depends(get_db),
) -> User:
    """MAJ position GPS ; marque onboarded si secteur déjà connu."""
    user.latitude = coords.latitude
    user.longitude = coords.longitude
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
) -> User:
    """MAJ secteur ; marque onboarded si géoloc déjà connue."""
    user.sector = payload.sector
    if user.latitude is not None and user.longitude is not None:
        user.onboarded = True
    await db.commit()
    await db.refresh(user)
    return user
