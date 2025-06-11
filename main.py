from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.core.security import enforce_x_user_id
from app.api.v1.auth import router as auth_router
from app.api.v1.clients import router as clients_router
from app.api.v1.stats import router as stats_router
from app.api.v1.prep import router as prep_router
from app.core.ws_manager import manager
from app.api.v1.catalog import router as catalog_router

app = FastAPI()

# Middleware global
app.middleware("http")(enforce_x_user_id)

# API routes
app.include_router(auth_router)
app.include_router(clients_router)
app.include_router(stats_router)
app.include_router(prep_router)
app.include_router(catalog_router)

@app.websocket("/ws/prep/{user_id}")
async def ws_prep(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id)