from fastapi import WebSocket
from typing import Dict, List
from app.core.logger import get_logger

logger = get_logger("WebSocketManager")

class ConnectionManager:
    def __init__(self):
        
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        
        self.active_connections[room_id].append(websocket)
        logger.info(f"Client con to rom {room_id}. Total clients: {len(self.active_connections[room_id])}")
        
        
        await self.broadcast_system_message(f"A new user joined the room.", room_id)

    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.active_connections:
            if websocket in self.active_connections[room_id]:
                self.active_connections[room_id].remove(websocket)
                logger.info(f"Client disconnected from Room {room_id}")
            
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast_code(self, message: str, room_id: str, sender: WebSocket):
        
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                if connection != sender:
                    await connection.send_text(message)

    async def broadcast_system_message(self, message: str, room_id: str):
        
        if room_id in self.active_connections:
            
            system_msg = "SYSTEM:" + message
            for connection in self.active_connections[room_id]:
                await connection.send_text(system_msg)


manager = ConnectionManager()