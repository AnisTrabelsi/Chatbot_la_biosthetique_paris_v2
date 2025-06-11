# app/services/pdf_service.py

from docx2pdf import convert  # ou importer la bonne librairie
from pathlib import Path

def convert_to_pdf(docx_path: str) -> str:
    """
    Convertit un fichier DOCX en PDF.
    Utilise docx2pdf pour générer le PDF à côté.
    """
    pdf_path = Path(docx_path).with_suffix(".pdf")
    convert(docx_path, str(pdf_path))
    return str(pdf_path)
