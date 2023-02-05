from fastapi import WebSocket
import logging
from typing import List

logger = logging.getLogger(__name__)


class SocketManager:
    def __init__(self):
        self.active_connections: List[(WebSocket, str)] = []

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        self.active_connections.append((websocket, room))

    def disconnect(self, websocket: WebSocket, room: str):
        try:
            self.active_connections.remove((websocket, room))
        except:
            pass

    async def send_personal_message(self, message: str, websocket: WebSocket, sender: str, room_name: str):
        await websocket.send_text(message)

    async def broadcast(self, data):
        print("\n [LOG] from broadcast function in SocketManager: \t", data, "\n")
        for connection in self.active_connections:
            await connection[0].send_json(data)


socket = SocketManager()
