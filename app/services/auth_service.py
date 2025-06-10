import secrets

async def authenticate_with_portatour(login: str, password: str) -> str:
    # TODO: appel réel plus tard
    if login and password:
        return secrets.token_urlsafe(32)
    raise ValueError("Invalid credentials")
