"""
Regroupe l’ensemble des modèles pour que SQLAlchemy crée les tables
lors de l’appel à `Base.metadata.create_all`.
"""

from .user import User
from .client import Client
from .invoice import Invoice

# -- le fichier peut s’appeler « catalog.py » ou « catalog_pdf.py »
try:
    from .catalog import CatalogPDF                    # type: ignore
except ModuleNotFoundError:                            # pragma: no cover
    from .catalog_pdf import CatalogPDF                # type: ignore

from .session import WASession

__all__ = [
    "User",
    "Client",
    "Invoice",
    "CatalogPDF",
    "WASession",
]
