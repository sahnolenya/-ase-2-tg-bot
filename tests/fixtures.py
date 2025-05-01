import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import Message, CallbackQuery
from aiogram import Router

@pytest.fixture
def mock_bot():
    """Mock bot"""
    with patch('main.Bot') as mock_bot_cls:
        mock_bot_instance = AsyncMock()
        mock_bot_instance.set_my_commands = AsyncMock()
        mock_bot_cls.return_value = mock_bot_instance
        yield mock_bot_instance

@pytest.fixture()
def mock_set_my_commands():
    """Mock создание меню"""
    with patch("main.set_my_commands", new_callable=AsyncMock) as mock:
        yield mock

@pytest.fixture
def mock_dispatcher():
    """Mock диспетчер"""
    with patch("main.Dispatcher") as mock_dispatcher_cls:
        mock_dispatcher_instance = AsyncMock()
        mock_dispatcher_instance.start_polling = AsyncMock()
        mock_dispatcher_cls.return_value = mock_dispatcher_instance
        yield mock_dispatcher_instance

@pytest.fixture
def mock_message():
    """Mock сообщение"""
    mock_msg = AsyncMock(spec=Message)
    mock_msg.answer = AsyncMock()
    mock_msg.from_user = AsyncMock()
    mock_msg.from_user.id = 123
    mock_msg.from_user.username = "test_user"
    mock_msg.text = ""
    return mock_msg

@pytest.fixture
def mock_callback():
    """Mock коллбэк"""
    mock_cb = AsyncMock(spec=CallbackQuery)
    mock_cb.message = AsyncMock(spec=Message)
    mock_cb.message.answer = AsyncMock()
    mock_cb.data = ""
    mock_cb.from_user = AsyncMock()
    mock_cb.from_user.id = 123
    mock_cb.answer = AsyncMock()
    return mock_cb

@pytest.fixture
def mock_router():
    """Mock роутер"""
    router = Router()
    return router
