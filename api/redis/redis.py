from redis import asyncio as aioredis

from api.config import RedisSettings
from redis.commands.json.path import Path

#settings = RedisSettings('localhost:6379')

class Redis:
    """
    config для подключения Redis
    """

    def __init__(self):
        self.connection_url = 'redis://localhost:6379'

    async def __aenter__(self):
        self.connection = aioredis.from_url(self.connection_url, db=0)

    async def __aexit__(self, *args):
        await self.connection.close()

    async def get(self, key: str) -> str:
        result = await self.connection.get(key)
        if result:
            return result.decode()

    async def set(self, key: str, value: str, ex: int = None):
        result = await self.connection.json().set(key, Path.root_path(), value)
        return result

    async def is_exist(self, key:str) -> int | None:
        isExists = await self.connection.exists(key)
        return isExists