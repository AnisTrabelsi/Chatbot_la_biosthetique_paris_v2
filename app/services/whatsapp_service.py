# app/services/whatsapp_service.py

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.session import WASession

async def create_wa_session(
    db: AsyncSession,
    phone_number: str,
    user_id: Optional[str] = None,
) -> WASession:
    """
    Ouvre ou récupère une session WhatsApp pour un commercial.
    """
    # mode eager (db=None) → on simule juste une session en mémoire
    if db is None:
        session = WASession(phone_number=phone_number)
    else:
        # cherche une session existante non fermée
        result = await db.execute(
            select(WASession)
            .where(WASession.phone_number == phone_number)
            .where(WASession.is_closed == False)
        )
        session = result.scalar_one_or_none()
        if not session:
            session = WASession(phone_number=phone_number)
            db.add(session)
            await db.commit()
            await db.refresh(session)

    # rattache le commercial si on a un user_id
    if user_id is not None:
        session.user_id = user_id
        if db is not None:
            db.add(session)
            await db.commit()

    return session


async def send_text(phone_number: str, text: str) -> None:
    """
    Envoie un message texte via WhatsApp.
    À vous de remplacer l'implémentation par votre client WhatsApp.
    """
    # ex. call à votre API WhatsApp ici
    ...


async def send_document(phone_number: str, document_url: str, filename: str) -> None:
    """
    Envoie un document (PDF, DOCX…) via WhatsApp.
    - document_url : URL signée MinIO ou autre
    - filename     : nom du fichier côté client
    """
    # ex. call à votre API WhatsApp ici
    ...
