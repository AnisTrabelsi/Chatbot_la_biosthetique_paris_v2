from uuid import uuid4
from pathlib import Path
from datetime import datetime, UTC

from fastapi import APIRouter, UploadFile, File, Form, Header, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceRead
from app.tasks.invoice import parse_invoice_pdf_task
from app.db.session import get_db

router = APIRouter(prefix="/v1/invoices", tags=["invoices"])

_UPLOAD_DIR = Path("/tmp/uploads/invoices")
_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("", response_model=InvoiceRead)
async def upload_invoice(
    client_id: str = Form(...),
    file: UploadFile = File(...),
    x_user_id: str = Header(..., alias="X-User-ID"),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF allowed")

    invoice_id = str(uuid4())
    file_path = _UPLOAD_DIR / f"{invoice_id}.pdf"
    file_path.write_bytes(await file.read())

    inv = Invoice(
        id=invoice_id,
        client_id=client_id,
        filename=file.filename,
        file_path=str(file_path),
        uploaded_at=datetime.now(UTC),
        meta={},
    )
    db.add(inv)
    await db.commit()
    await db.refresh(inv)

    parse_invoice_pdf_task.delay(invoice_id, str(file_path))
    return inv


@router.get("/{invoice_id}", response_model=InvoiceRead)
async def get_invoice(invoice_id: str, db: AsyncSession = Depends(get_db)):
    inv = await db.get(Invoice, invoice_id)
    if not inv:
        raise HTTPException(404, "Invoice not found")
    return inv
