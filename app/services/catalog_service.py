# app/services/catalog_service.py
"""
Service pour parser les PDF de catalogue et en extraire les métadonnées.
"""
import io
import pdfplumber
from typing import Dict

async def parse_pdf_metadata(file_bytes: bytes) -> Dict:
    """
    Extrait un texte brut des pages PDF et renvoie des métadonnées minimalistes.
    """
    # Extraction du texte avec pdfplumber
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    # Stub : retourne la longueur du texte et le premier paragraphe
    return {"length": len(text), "excerpt": text.splitlines()[0] if text else ""}
