from fastapi import APIRouter

from api.redis.redis import Redis
from api.schemas.chatDTO import Chat
from redis.commands.json.path import Path
import json

router = APIRouter()

redis = Redis()

@router.post("/save")
async def save_messages(telegram_id: str, messages: list[str]):

    chat_session = Chat(
        telegram_id=telegram_id,
        messages=[],
    )
    print(chat_session)
    async with redis:
        await redis.set(key = str(telegram_id), value = chat_session.model_dump())
        
    
    return {"status": 200, "telegram_id": telegram_id}