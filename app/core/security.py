from fastapi import Request
from starlette.responses import JSONResponse

async def enforce_x_user_id(request: Request, call_next):
    user_id = request.headers.get("X-User-ID")
    if not user_id:
        # Retourne directement une réponse 401 JSON, sans lever d'exception
        return JSONResponse(
            status_code=401,
            content={"detail": "Missing X-User-ID header"}
        )
    return await call_next(request)
