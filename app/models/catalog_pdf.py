from sqlalchemy import Column, String, Integer, JSON
from app.db.base import Base


class CatalogPDF(Base):
    """
    Table stockant les PDF « catalogue ».

    ⚠️  On NE PEUT PAS utiliser le nom « metadata » en Declarative ;
    on le remplace donc par « meta ».
    """
    __tablename__ = "catalog_pdfs"

    id: str = Column(String, primary_key=True)
    doc_type: str = Column(String, nullable=False)
    filename: str = Column(String, nullable=False)
    version: int = Column(Integer, nullable=False)
    meta: dict = Column(JSON, default=dict)          # ← colonne valide
