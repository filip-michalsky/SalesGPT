from fastapi import Depends, HTTPException, status
from redis.redis import Redis

async def check_telegram_id(telegram_id: str = None):
    if not telegram_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Telegram ID is required")

    redis = Redis()
    async with redis:
        exists = await redis.is_exist(telegram_id)
        if not exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token not found in Redis")

    return telegram_id
