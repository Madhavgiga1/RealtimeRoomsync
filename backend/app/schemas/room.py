from pydantic import BaseModel
from typing import Optional

class RoomCreate(BaseModel):
    pass

class RoomResponse(BaseModel):
    roomId: str

class AutocompleteRequest(BaseModel):
    code: str
    cursorPosition: int
    language: str

class AutocompleteResponse(BaseModel):
    suggestion: str