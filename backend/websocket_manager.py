# websocket_manager.py
from fastapi import WebSocket

connected_clients = {}

async def connect_client(websocket: WebSocket,client_id):
    if client_id not in connected_clients:
        connected_clients[client_id] = []
    await websocket.accept()
    connected_clients[client_id].append(websocket)

def disconnect_client(websocket: WebSocket,client_id):
    connected_clients[client_id].remove(websocket)

async def notify_client(client_id,text):
    await connected_clients[client_id].send_text(f"{text}")
