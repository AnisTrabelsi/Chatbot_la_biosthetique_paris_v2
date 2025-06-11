import io
from typing import Dict
from datetime import datetime
from pytesseract import image_to_string
from pdf2image import convert_from_bytes
from app.services.prep_service import build_docx  # compatibility
__all__ = ["parse_invoice_pdf", "build_docx"]

async def parse_invoice_pdf(file_bytes: bytes) -> Dict:
    """
    Extrait le texte d'une facture PDF via OCR (pdf2image + pytesseract),
    puis tente de trouver le montant et la date. Ici, stub de démonstration.
    """
    # Convertir les pages PDF en images
    images = convert_from_bytes(file_bytes)
    full_text = "".join(image_to_string(img) for img in images)

    # Recherche simplifiée de montant et date
    amount = None
    date = None
    for line in full_text.splitlines():
        if '$' in line:
            amount = line.strip()
        if '/' in line and len(line.split('/')[0]) <= 2:
            date = line.strip()
    return {"amount": amount or "unknown", "date": date or datetime.utcnow().isoformat()}
