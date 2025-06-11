# app/db/session.py
from __future__ import annotations

import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# --------------------------------------------------------------------------- #
# 1) URL de connexion — sqlite par défaut pour le dev, PostgreSQL en prod
# --------------------------------------------------------------------------- #
#  ↳ Les deux noms ci-dessous pointent vers la même valeur :
#       • DATABASE_URL                 – utilisé par FastAPI / tests
#       • SQLALCHEMY_DATABASE_URL      – attendu par alembic/env.py
# --------------------------------------------------------------------------- #
SQLALCHEMY_DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./dev.db",
)
DATABASE_URL: str = SQLALCHEMY_DATABASE_URL  # alias rétro-compatibilité

# --------------------------------------------------------------------------- #
# 2) Engine asynchrone
# --------------------------------------------------------------------------- #
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,          # passez à True pour le debug SQL
    future=True,
)

# --------------------------------------------------------------------------- #
# 3) Session factory
# --------------------------------------------------------------------------- #
AsyncSessionLocal: sessionmaker[AsyncSession] = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# --------------------------------------------------------------------------- #
# 4) Dépendance FastAPI
# --------------------------------------------------------------------------- #
async def get_db() -> AsyncSession:  # pragma: no cover
    """
    Dépendance FastAPI : ouvre une session asynchrone et la ferme proprement.
    Usage →
        async def route(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        yield session
