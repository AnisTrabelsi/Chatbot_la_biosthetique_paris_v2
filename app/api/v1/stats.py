from fastapi import APIRouter, UploadFile, File, Form, Header, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.excel_service import parse_stats_excel
from app.db.session import get_db

router = APIRouter(prefix="/v1/stats", tags=["stats"])

@router.post("/upload", response_model=list[dict])
async def upload_stats(
    kdnr: str = Form(...),
    file: UploadFile = File(...),
    x_user_id: str = Header(..., alias="X-User-ID"),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(400, "Invalid file type")
    content = await file.read()
    stats_objects = await parse_stats_excel(content, kdnr, db)
    return [{"id": s.id, "kdnr": s.kdnr} for s in stats_objects]
