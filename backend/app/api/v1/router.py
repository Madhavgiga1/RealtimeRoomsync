from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.room import RoomResponse, AutocompleteRequest, AutocompleteResponse
from app.services import room_service
from app.services.websocket_manager import manager
from app.core.logger import get_logger
import asyncio

router = APIRouter()
logger = get_logger("API_Router")


def generate_mock_suggestion(code: str) -> str:
    
    code_stripped = code.strip().lower()
    if code_stripped.endswith("def"):
        return " my_function():\n    '''Docstring'''\n    pass"
    elif "import" in code_stripped:
        return " os, sys, json"
    elif "class" in code_stripped:
        return " MyClass:\n    def __init__(self):\n        pass"
    elif "print" in code_stripped:
        return "('Hello World')"
    return ""



@router.post("/rooms", response_model=RoomResponse)
async def create_room(db: AsyncSession = Depends(get_db)):
    logger.info("Creating a new room")
    room = await room_service.create_new_room(db)
    return {"roomId": room.id}

@router.post("/autocomplete", response_model=AutocompleteResponse)
async def get_autocomplete(payload: AutocompleteRequest):
   
    await asyncio.sleep(0.1)
    
    suggestion = generate_mock_suggestion(payload.code)
    return {"suggestion": suggestion}

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    room_id: str, 
    db: AsyncSession = Depends(get_db)
):
    # Validate room existence
    room = await room_service.get_room(db, room_id)
    if not room:
        logger.warning(f"Attempted connection to invalid room: {room_id}")
        await websocket.close()
        return

    await manager.connect(websocket, room_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            
            await manager.broadcast_code(data, room_id, websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        await manager.broadcast_system_message("A user left the room.", room_id)