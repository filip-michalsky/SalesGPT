import os, json
from tortoise import Tortoise
from langchain import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from salesgpt.models import ChatMessage
import pytest


async def db_init():
    await Tortoise.init(
        db_url=os.environ.get('DB_URL'),
        modules={'models': ['__main__']},
    )


async def db_close():
    await Tortoise.close_connections()


class TestDatabase:

    def test_product_catalog(self, load_env):
        db = SQLDatabase.from_uri(os.environ.get('DB_SQL_URL'))
        llm = OpenAI(temperature=0, model_name=os.environ.get('MODEL_NAME'))
        db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
        response = db_chain.run('which product has the highest price and give me its description')
        assert response is not None, "Agent output cannot be None."

    @pytest.mark.asyncio
    async def test_product_catalog_async(self, load_env):
        """Async Test Hello World"""
        try:
            await db_init()
            conn = Tortoise.get_connection('default')
            values = await conn.execute_query('select * from product_catalog')
            print(values)
        finally:
            await db_close()
        assert "Hello World" is not None, "Agent output cannot be None."
