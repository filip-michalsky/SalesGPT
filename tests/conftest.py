import os
from tortoise import Tortoise, run_async
import pytest
from dotenv import load_dotenv


async def init_db():
    await Tortoise.init(
        db_url=os.environ.get('DB_URL'),
        modules={'models': ['salesgpt.models']},
    )


async def db_close():
    await Tortoise.close_connections()


@pytest.fixture
def load_env():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")
    load_dotenv(dotenv_path=f"{data_dir}/.env")
    run_async(init_db())
