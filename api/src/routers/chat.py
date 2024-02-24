from fastapi import APIRouter

from api.redis.redis import Redis
from api.schemas.chatDTO import Chat

router = APIRouter(
    prefix="/tokens"
)

redis = Redis()

@router.post("")
async def save_messages(telegram_id: str):
    chat_session = Chat(
        messages=[],
    )
    async with redis:
        await redis.set(name = str(telegram_id), obj = chat_session.model_dump(), ex=3600)
    return {"telegram_id": telegram_id}