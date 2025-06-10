from docx2pdf import convert
from pathlib import Path

def convert_to_pdf(docx_path: str) -> str:
    pdf_path = Path(docx_path).with_suffix(".pdf")
    # docx2pdf convertit en place
    convert(docx_path, str(pdf_path))
    return str(pdf_path)
