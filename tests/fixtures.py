import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram.types import Message, CallbackQuery

@pytest.fixture
def mock_bot():
    mock = AsyncMock()
    mock.set_my_commands = AsyncMock()
    return mock

@pytest.fixture
def mock_dispatcher():
    mock = AsyncMock()
    mock.start_polling = AsyncMock()
    mock.include_router = MagicMock()
    return mock

@pytest.fixture
def mock_message():
    mock = AsyncMock(spec=Message)
    mock.answer = AsyncMock(return_value=None)
    mock.from_user = MagicMock()
    mock.from_user.id = 123
    mock.text = ""
    return mock

@pytest.fixture
def mock_callback():
    mock = AsyncMock(spec=CallbackQuery)
    mock.message = AsyncMock(spec=Message)
    mock.message.answer = AsyncMock(return_value=None)
    mock.data = ""
    mock.answer = AsyncMock(return_value=None)
    return mock