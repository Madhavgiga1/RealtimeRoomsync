from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base
import uuid

class Room(Base):
    __tablename__ = "rooms"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    code_content = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    