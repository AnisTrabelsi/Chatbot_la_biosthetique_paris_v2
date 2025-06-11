from pydantic import BaseModel, Field, ConfigDict


class CatalogPDFRead(BaseModel):
    """Schéma de sortie pour un PDF catalogue."""

    id: str
    doc_type: str
    filename: str
    version: int

    # ⚠️  En BDD la colonne s’appelle « meta ».
    #      On déclare donc l’attribut « meta » et on lui donne pour alias
    #      « metadata » – le nom attendu par la couche API et les tests.
    meta: dict = Field(default_factory=dict, alias="metadata")

    # ——————————————————————————————————————————
    # Réglages Pydantic ( v-2 )
    # ——————————————————————————————————————————
    model_config = ConfigDict(
        from_attributes=True,      # remplir à partir d’un ORM
        populate_by_name=True,     # accepter metadata **ou** meta en entrée
    )
