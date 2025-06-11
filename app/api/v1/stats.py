# app/api/v1/stats.py
from fastapi import APIRouter, UploadFile, File, Form, Header, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.excel_service import parse_stats_excel
from app.db.session import get_db

router = APIRouter(prefix="/v1/stats", tags=["stats"])

@router.post(
    "/upload",
    response_model=list[dict],
    status_code=status.HTTP_200_OK,
)
async def upload_stats(
    kdnr: str = Form(...),
    file: UploadFile = File(...),
    x_user_id: str = Header(..., alias="X-User-ID"),
    db: AsyncSession = Depends(get_db),
):
    # Vérifie le type de fichier
    if not file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid file type")
    content = await file.read()
    # délègue au service, qui doit lever HTTPException(404) si client inconnu
    stats_objects = await parse_stats_excel(content, kdnr, db)
    return [{"id": s.id, "kdnr": s.kdnr} for s in stats_objects]
