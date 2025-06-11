import phonenumbers
from typing import Tuple, Dict
import random

async def enrich_lead_data(phone_number: str) -> Tuple[Dict, str]:
    """
    Stub : normalise le numéro, simule un score et des données.
    """
    pn = phonenumbers.parse(phone_number, None)
    norm = phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164)
    data = {"normalized": norm, "source": "whatsapp"}
    score = random.choice(["hot", "warm", "cold"])
    return data, score
