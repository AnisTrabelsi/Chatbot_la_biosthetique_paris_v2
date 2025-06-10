from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.prep import PrepFullRequest, PrepFullResponse
from app.api.deps import get_current_user
from app.db.session import get_db
from app.tasks.llm import prep_visit_task

router = APIRouter(prefix="/v1/prep", tags=["prep"])

@router.post("/full", response_model=PrepFullResponse)
async def prep_full(
    body: PrepFullRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    import uuid
    prep_id = str(uuid.uuid4())
    prep_visit_task.delay(prep_id, current_user.id, body.client_id)
    return {"prep_id": prep_id}
