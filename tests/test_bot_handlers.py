import pytest
from unittest.mock import patch
from aiogram.types import InlineKeyboardMarkup
from handlers.handlers import (
    process_start_command,
    handle_news,
    yandex_news,
    rbc_news,
    ria_news,
    help_command,
    register_message_handlers
)
from handlers.callbacks import callback_help, callback_message
from tests.fixtures import mock_message, mock_callback, mock_dispatcher

@pytest.mark.asyncio
async def test_process_start_command(mock_message):
    mock_message.text = "/start"
    await process_start_command(mock_message)
    mock_message.answer.assert_called_once()
    args = mock_message.answer.call_args[0]
    kwargs = mock_message.answer.call_args[1]
    assert "Привет, давай посмотрим новости!" in (args[0] if args else kwargs.get('text', ''))

@pytest.mark.asyncio
async def test_handle_news(mock_message):
    mock_message.text = "Новости"
    await handle_news(mock_message)
    mock_message.answer.assert_called_once()
    args = mock_message.answer.call_args[0]
    kwargs = mock_message.answer.call_args[1]
    assert "Где вы хотите посмотреть новости?" in (args[0] if args else kwargs.get('text', ''))

@pytest.mark.asyncio
async def test_yandex_news(mock_message):
    mock_message.text = "Яндекс Дзен"
    await yandex_news(mock_message)
    mock_message.answer.assert_called_once()
    args = mock_message.answer.call_args[0]
    kwargs = mock_message.answer.call_args[1]
    assert "Яндекс Дзен" in (args[0] if args else kwargs.get('text', ''))
    assert "dzen.ru" in (args[0].lower() if args else kwargs.get('text', '').lower())
    assert (not kwargs) or kwargs.get('parse_mode') == "Markdown"

@pytest.mark.asyncio
async def test_rbc_news(mock_message):
    mock_message.text = "Новости РБК"
    await rbc_news(mock_message)
    mock_message.answer.assert_called_once()
    args = mock_message.answer.call_args[0]
    kwargs = mock_message.answer.call_args[1]
    assert "РБК" in (args[0] if args else kwargs.get('text', ''))
    assert "rbc.ru" in (args[0].lower() if args else kwargs.get('text', '').lower())
    assert (not kwargs) or kwargs.get('parse_mode') == "Markdown"

@pytest.mark.asyncio
async def test_ria_news(mock_message):
    mock_message.text = "РИА Новости"
    await ria_news(mock_message)
    mock_message.answer.assert_called_once()
    args = mock_message.answer.call_args[0]
    kwargs = mock_message.answer.call_args[1]
    assert "РИА Новости" in (args[0] if args else kwargs.get('text', ''))
    assert "ria.ru" in (args[0].lower() if args else kwargs.get('text', '').lower())
    assert (not kwargs) or kwargs.get('parse_mode') == "Markdown"

@pytest.mark.asyncio
async def test_help_command(mock_message):
    mock_message.text = "help"
    await help_command(mock_message)
    mock_message.answer.assert_called_once()
    args = mock_message.answer.call_args[0]
    kwargs = mock_message.answer.call_args[1]
    assert "Это бот для просмотра новостей" in (args[0] if args else kwargs.get('text', ''))
    assert "/start" in (args[0] if args else kwargs.get('text', ''))
    assert "Новости" in (args[0] if args else kwargs.get('text', ''))

@pytest.mark.asyncio
async def test_callback_help(mock_callback):
    await callback_help(mock_callback)
    mock_callback.answer.assert_called_once()
    mock_callback.message.answer.assert_called_once_with("Это помощь по боту")

@pytest.mark.asyncio
async def test_callback_message_help(mock_callback):
    mock_callback.data = "help"
    await callback_message(mock_callback)
    mock_callback.answer.assert_called_once()
    mock_callback.message.answer.assert_called_once_with("Это помощь по боту")

@pytest.mark.asyncio
async def test_register_message_handlers(mock_dispatcher):
    register_message_handlers(mock_dispatcher)
    mock_dispatcher.include_router.assert_called_once()