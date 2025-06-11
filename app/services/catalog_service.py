import pdfplumber
from typing import Dict

async def parse_pdf_metadata(file_bytes: bytes) -> Dict:
    # Lecture texte simple
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    # Extraction tables (facultatif)
    # tables = [table.df.to_dict() for table in pdf.pages[0].extract_tables()]
    # Appel LLM pour extraire les infos clés
    # ex.: offres, durée, prix, format…
    # stub : on renvoie la longueur du texte
    return {"length": len(text), "excerpt": text[:200]}
