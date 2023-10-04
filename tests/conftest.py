import os

import pytest
from dotenv import load_dotenv


@pytest.fixture
def load_env():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")
    load_dotenv(dotenv_path=f"{data_dir}/.env")
