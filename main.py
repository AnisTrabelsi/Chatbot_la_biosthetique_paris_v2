from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.core.security import enforce_x_user_id
from app.api.v1.auth import router as auth_router
from app.api.v1.clients import router as clients_router
from app.api.v1.stats import router as stats_router
from app.api.v1.prep import router as prep_router
from app.api.v1.catalog import router as catalog_router
from app.core.ws_manager import manager
from app.api.v1.invoices import router as invoices_router
from app.services.prep_service import build_docx
from app.api.v1.webhook import router as webhook_router
from app.api.v1.invoices import router as invoices_router
from app.api.v1.auth import router as auth_router
from app.api.v1.sessions import router as sessions_router

from app.api.v1 import auth, users, clients, stats, prep, catalog, invoices, webhook
app = FastAPI()

# Middleware global
app.middleware("http")(enforce_x_user_id)

# API routes
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(clients.router)
app.include_router(stats.router)
app.include_router(prep.router)
app.include_router(catalog.router)
app.include_router(invoices.router)
app.include_router(webhook.router)
app.include_router(auth_router)
app.include_router(sessions_router)

# WebSocket pour notifications de préparation
@app.websocket("/ws/prep/{user_id}")
async def ws_prep(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id)

# WebSocket pour notifications de prospection
@app.websocket("/ws/prospect/{phone_number}")
async def ws_prospect(websocket: WebSocket, phone_number: str):
    await manager.connect(phone_number, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(phone_number)
