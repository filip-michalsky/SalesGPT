import json

from redis import asyncio as aioredis

from api.config import RedisSettings

settings = RedisSettings()


class Redis:
    """
    config для подключения Redis
    """

    def __init__(self):
        self.connection_url = f'redis://{settings.url}'

    async def __aenter__(self):
        self.connection = aioredis.from_url(self.connection_url, db=0)

    async def __aexit__(self, *args):
        await self.connection.close()

    async def get(self, name: str) -> json:
        result = await self.connection.json().get(name=name)
        return result

    async def set(self, key: str, value: str, ex: int = None):
        result = await self.connection.set(name=key, value=value, ex=ex)
        return result

    async def is_exist(self, key:str) -> int | None:
        isExists = await self.connection.exists(key)
        return isExists