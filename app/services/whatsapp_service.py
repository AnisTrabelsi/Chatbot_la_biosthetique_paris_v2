from app.models.session import WASession
from app.models.lead_enrichment import LeadEnrichment
from app.db.session import AsyncSessionLocal

async def create_wa_session(db, phone_number: str) -> WASession:
    session = WASession(phone_number=phone_number)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session
