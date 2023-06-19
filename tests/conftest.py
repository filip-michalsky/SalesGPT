import os

import pytest


@pytest.fixture
def test_data_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")

