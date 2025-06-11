import os
from cryptography.fernet import Fernet

# La clé FERNET_KEY doit être définie dans votre .env
key = os.getenv("FERNET_KEY")
if not key:
    raise RuntimeError("FERNET_KEY must be set in environment")
fernet = Fernet(key.encode())
