import json

from redis import asyncio as aioredis

from api.config import RedisSettings
from redis.commands.json.path import Path

settings = RedisSettings()

class Redis:
    """
    config для подключения Redis
    """

    def __init__(self):
        self.connection_url = settings.url

    async def __aenter__(self):
        self.connection = aioredis.from_url(self.connection_url, db=0)

    async def __aexit__(self, *args):
        await self.connection.close()

    async def get(self, name: str) -> json:
        result = await self.connection.json().get(name=name)
        return result

    async def set(self, name: str, obj: dict, ex: int = None):
        result = await self.connection.json().set(name = name,path=Path.root_path(), obj=obj)
        if ex:
            await self.connection.expire(str(name), ex)
        return result

    async def is_exist(self, key:str) -> int | None:
        isExists = await self.connection.exists(key)
        return isExists