from fastapi import APIRouter, Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.whatsapp_service import create_wa_session
from app.tasks.lead import enrich_lead_task
from app.db.session import get_db
from phonenumbers import parse as parse_phone, NumberParseException

router = APIRouter(prefix="/v1/webhook", tags=["webhook"])

class WASessionCloseRequest(BaseModel):
    pass  # option de fermeture

@router.post("/wa")
async def wa_webhook(
    payload: dict,
    x_user_id: str = Header(..., alias="X-User-ID"),
    db: AsyncSession = Depends(get_db),
):
    # extraire numéro depuis payload, ex: payload["from"]
    phone = payload.get("from")
    try:
        pn = parse_phone(phone, None)
    except NumberParseException:
        raise HTTPException(400, "Invalid phone number")
    session = await create_wa_session(db, phone)
    # déclencher enrichissement
    enrich_lead_task.delay(session.id, phone)
    return {"session_id": session.id}
