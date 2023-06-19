import os

import pytest


@pytest.fixture
def test_data_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")


@pytest.fixture
def load_env():
    data_dir = test_data_dir()

    with open(f'{data_dir}/test.env','r') as f:
            env_file = f.readlines()
    envs_dict = {key.strip("'") :value.strip("\n") for key, value in [(i.split('=')) for i in env_file]}
    os.environ['OPENAI_API_KEY'] = envs_dict['OPENAI_API_KEY']