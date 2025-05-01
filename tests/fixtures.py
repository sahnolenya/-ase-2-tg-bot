
import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import Message
from aiogram import Router

# Фикстуры в pytest позволяют выносить в отдельные функции типовые действия
# например: настройка тестового окружения, создание тестовых данных, выполнение завершающие действия
# https://habr.com/ru/articles/731296/

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
    """Моск создание меню"""
    with patch(target: "main.set_my_commands", new_callable=AsyncMock) as mock:
    yield mock_set_my_commands

@pytest.fixture
def mock_dispatcher():
    """Моск диспетчер"""
    with patch("main. Dispatcher") as mock_dispatcher_cls:
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
    mock_msg.from_user.id = AsyncMock()
    mock_msg.from_user.username = AsyncMock()
    return mock_msg

@pytest.fixture
def mock_router():
    """Mock роутер"""
    router = Router()
    return router