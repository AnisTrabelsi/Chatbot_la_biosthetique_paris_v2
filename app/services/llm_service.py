# app/services/llm_service.py
"""
Service pour générer le prompt de préparation de visite via LLM (OpenAI).
"""
from typing import Dict

# Stub asynchrone
async def enrich_visit_prompt(client_data: Dict) -> str:
    """
    Génére un prompt texte à envoyer à l'LLM à partir des données client.
    Dans un vrai cas, on ferait appel à OpenAI ou autre.
    Ici, on renvoie un prompt simple pour stub.
    """
    # Exemple de construction de prompt
    name = client_data.get("name", "")
    kdnr = client_data.get("kdnr", "")
    prompt = (
        f"Prépare une visite pour le client {name} (Kdnr: {kdnr}). "
        "Détaille les points clés à aborder en réunion."
    )
    return prompt
