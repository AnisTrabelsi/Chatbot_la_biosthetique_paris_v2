# app/core/ws_manager.py
from typing import Dict
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active: Dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active[user_id] = websocket

    def disconnect(self, user_id: str):
        self.active.pop(user_id, None)

    async def notify_prep_ready(self, user_id: str, prep_id: str, pdf_path: str):
        ws = self.active.get(user_id)
        if ws:
            await ws.send_json({
                "event": "prep_ready",
                "prep_id": prep_id,
                "pdf_path": pdf_path,
            })

manager = ConnectionManager()
