from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.schemas.prep import (
    DocsMeta,           # déjà utilisé plus haut
    PrepFullRequest,
    PrepFullResponse,
)
from app.api.deps import get_current_user           # <- dépendance centrale
from app.tasks.llm import prep_visit_task           # Celery task
from app.schemas.prep import DocsMeta
# app/api/v1/prep.py
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db        # ← AJOUT ICI
from app.schemas.prep import DocsMeta, PrepFullRequest, PrepFullResponse
from app.api.deps import get_current_user
from app.tasks.llm import prep_visit_task

router = APIRouter(prefix="/v1/prep", tags=["prep"])

# … /docs-meta ici …
@router.get("/docs-meta", response_model=DocsMeta)
async def docs_meta(client_id: str, db: AsyncSession = Depends(get_db)):
    """
    Retourne la disponibilité des différents documents pour l’interface « Hub ».
    Pour l’instant : stub = tous False.
    """
    return DocsMeta(stats=False, offer_pdf=False, training_pdf=False, invoices=False)

@router.post(
    "/full",
    response_model=PrepFullResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Lance la préparation de visite complète",
)
async def prep_full(
    payload: PrepFullRequest,
    current_user = Depends(get_current_user),
):
    """
    ① génère un `prep_id`  
    ② déclenche la *pipeline* Celery (`prep_visit_task`)  
    ③ répond immédiatement 202 + prep_id
    """
    prep_id = str(uuid.uuid4())
    #                prep_id,   user_id,          client_id
    prep_visit_task.delay(prep_id, current_user.id, payload.client_id)
    return {"prep_id": prep_id}
