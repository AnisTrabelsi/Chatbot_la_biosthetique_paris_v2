from fastapi import APIRouter, Header, Depends, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from phonenumbers import parse as parse_phone, NumberParseException

import app.services.whatsapp_service as whatsapp_service
from app.tasks.lead import enrich_lead_task
from app.db.session import get_db
from app.core.ws_manager import manager

router = APIRouter(prefix="/v1/webhook", tags=["webhook"])


class WASessionCloseRequest(BaseModel):
    """Schéma pour fermeture de session (optionnel)."""
    pass


@router.post("/wa")
async def wa_webhook(
    payload: dict,
    x_user_id: str = Header(..., alias="X-User-ID"),
    db: AsyncSession = Depends(get_db),
):
    phone = payload.get("from")
    try:
        pn = parse_phone(phone, None)
    except NumberParseException:
        raise HTTPException(400, "Invalid phone number")

    # 1. créer la session WASession
    session = await whatsapp_service.create_wa_session(db, phone)

    # 2. lancer le traitement asynchrone
    enrich_lead_task.delay(session.id, phone)

    return {"session_id": session.id}


@router.websocket("/ws/wa/{phone_number}")
async def ws_whatsapp(websocket: WebSocket, phone_number: str):
    await manager.connect(phone_number, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(phone_number)
