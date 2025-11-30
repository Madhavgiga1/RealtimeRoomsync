from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.room import Room

async def create_new_room(db: AsyncSession) -> Room:
    new_room = Room()
    db.add(new_room)
    await db.commit()
    await db.refresh(new_room)
    return new_room

async def get_room(db: AsyncSession, room_id: str) -> Room | None:
    result = await db.execute(select(Room).filter(Room.id == room_id))
    return result.scalars().first()

async def update_room_code(db: AsyncSession, room_id: str, code: str):
    room = await get_room(db, room_id)
    if room:
        room.code_content = code
        await db.commit()