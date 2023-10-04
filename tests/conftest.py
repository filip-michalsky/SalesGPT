import os
from dotenv import load_dotenv
import pytest


@pytest.fixture
def load_env():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")
    load_dotenv(dotenv_path=f"{data_dir}/.env")

