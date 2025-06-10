from fastapi import FastAPI
from app.api.v1.clients import router as clients_router
from app.core.security import enforce_x_user_id
app = FastAPI()
from app.api.v1.auth import router as auth_router
@app.get("/ping")
async def pong():
    return {"ping": "pong"}


app.include_router(clients_router)
app.middleware("http")(enforce_x_user_id)
app.include_router(auth_router)
