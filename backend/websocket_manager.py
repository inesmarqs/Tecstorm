# websocket_manager.py
from fastapi import WebSocket
from typing import List

connected_clients: List[WebSocket] = []

async def connect_client(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

def disconnect_client(websocket: WebSocket):
    connected_clients.remove(websocket)

async def notify_clients(barcode: str):
    for client in connected_clients:
        await client.send_text(f"{barcode}")
