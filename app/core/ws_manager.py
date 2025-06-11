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

    async def notify_prospect_ready(self, phone_number: str, session_id: str, enrichment: dict):
        ws = self.active.get(phone_number)
        if ws:
            await ws.send_json({
                "event": "prospect_ready",
                "session_id": session_id,
                "enrichment": enrichment,
            })

manager = ConnectionManager()
