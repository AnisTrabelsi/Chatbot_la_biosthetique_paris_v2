import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# URL async pour l'application (asyncpg)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://fastapi_user:fastapi_pass@localhost:5432/fastapi_user",
)

# Engine asynchrone
engine = create_async_engine(DATABASE_URL, echo=False, future=True)

# Factory de sessions
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncSession:
    """Dépendance FastAPI - renvoie une session puis la ferme."""
    async with AsyncSessionLocal() as session:
        yield session
