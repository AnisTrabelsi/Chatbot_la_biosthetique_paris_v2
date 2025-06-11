# app/services/pdf_service.py
"""Stub pour convertir un DOCX vers un PDF (mock)."""
from pathlib import Path

def convert_to_pdf(docx_path: str) -> str:
    pdf_path = Path(docx_path).with_suffix(".pdf")
    # Stub : crée un fichier vide .pdf à côté du docx
    pdf_path.touch()
    return str(pdf_path)
