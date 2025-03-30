# websocket_manager.py
from fastapi import WebSocket

connected_clients = {}

async def connect_client(websocket: WebSocket,client_id):
    if client_id not in connected_clients:
        connected_clients[client_id] = None
    await websocket.accept()
    connected_clients[client_id] = websocket
    print(f"Client {client_id} connected")

def disconnect_client(websocket, client_id):
    if client_id in connected_clients and isinstance(connected_clients[client_id], list):
        if websocket in connected_clients[client_id]:
            connected_clients[client_id].remove(websocket)

async def notify_client(client_id,text):
    print(f"Sending message to client {client_id}: {text}")
    await connected_clients[client_id].send_text(f"{text}")
