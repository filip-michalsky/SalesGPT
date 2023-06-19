import os

import pytest


@pytest.fixture
def load_env():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")

    with open(f"{data_dir}/.env", "r") as f:
        env_file = f.readlines()
    envs_dict = {
        key.strip("'"): value.strip("\n")
        for key, value in [(i.split("=")) for i in env_file]
    }
    os.environ["OPENAI_API_KEY"] = envs_dict["OPENAI_API_KEY"]
