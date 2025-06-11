from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field
from phonenumbers import NumberParseException, parse as parse_phone
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services import whatsapp_service               # ← on importe le module
from app.tasks.lead import enrich_lead_task             # Celery task (lead)
from app.tasks.llm import prep_visit_task               # Celery task (prep)

router = APIRouter(prefix="/v1/webhook", tags=["webhook"])


class WAInbound(BaseModel):
    frm: str = Field(..., alias="from")
    text: str | None = Field(None, alias="text")        # optionnel


@router.post("/wa", status_code=status.HTTP_200_OK)
async def wa_webhook(
    payload: WAInbound,
    x_user_id: str = Header(..., alias="X-User-ID"),
    db: AsyncSession = Depends(get_db),
):
    # 1) validation du numéro
    try:
        parse_phone(payload.frm, None)
    except NumberParseException:
        raise HTTPException(400, "Invalid phone number")

    # 2) ouverture ou récupération de session WhatsApp
    session = await whatsapp_service.create_wa_session(db, payload.frm)

    # 3) pas de texte OU autre qu’une commande « /prep » → enrichissement Lead
    if not payload.text or not payload.text.lower().startswith("/prep"):
        enrich_lead_task.delay(session.id, payload.frm)
        return {"session_id": session.id}

    # 4) gestion de la commande « /prep <client_id> »
    parts = payload.text.split(maxsplit=1)
    if len(parts) != 2:
        await whatsapp_service.send_text(payload.frm, "❌ Usage : /prep <client_id>")
        raise HTTPException(400, "Bad command")

    client_id = parts[1]
    prep_id = str(uuid4())

    # Lancement du pipeline de préparation
    prep_visit_task.delay(prep_id, x_user_id, client_id)
    await whatsapp_service.send_text(
        payload.frm,
        f"🛠️ Préparation du client {client_id} lancée…",
    )

    return {"prep_id": prep_id}
