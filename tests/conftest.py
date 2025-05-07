import pytest
from unittest.mock import patch
import os

@pytest.fixture(autouse=True)
def mock_env():
    os.environ["BOT_TOKEN"] = "test_token"