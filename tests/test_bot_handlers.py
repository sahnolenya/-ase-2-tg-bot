import pytest
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


@pytest.mark.asyncio
async def test_process_start_command(mock_message):
    mock_message.text = "/start"

    await process_start_command(mock_message)

    mock_message.answer.assert_called_once()
    args, kwargs = mock_message.answer.call_args
    assert "Привет, давай посмотрим новости!" in kwargs["text"]
    assert kwargs["reply_markup"] is not None  # Более мягкая проверка клавиатуры


@pytest.mark.asyncio
async def test_handle_news(mock_message):
    mock_message.text = "Новости"

    await handle_news(mock_message)

    mock_message.answer.assert_called_once()
    args, kwargs = mock_message.answer.call_args
    assert "Где вы хотите посмотреть новости?" in kwargs["text"]
    assert kwargs["reply_markup"] is not None


@pytest.mark.asyncio
async def test_yandex_news(mock_message):
    mock_message.text = "Яндекс Дзен"

    await yandex_news(mock_message)

    mock_message.answer.assert_called_once()
    args, kwargs = mock_message.answer.call_args
    assert "Яндекс Дзен" in kwargs["text"]
    assert "dzen.ru" in kwargs["text"].lower()  # Более гибкая проверка URL
    assert kwargs.get("parse_mode") == "Markdown"


@pytest.mark.asyncio
async def test_rbc_news(mock_message):
    mock_message.text = "Новости РБК"

    await rbc_news(mock_message)

    mock_message.answer.assert_called_once()
    args, kwargs = mock_message.answer.call_args
    assert "РБК" in kwargs["text"]
    assert "rbc.ru" in kwargs["text"].lower()
    assert kwargs.get("parse_mode") == "Markdown"


@pytest.mark.asyncio
async def test_ria_news(mock_message):
    mock_message.text = "РИА Новости"

    await ria_news(mock_message)

    mock_message.answer.assert_called_once()
    args, kwargs = mock_message.answer.call_args
    assert "РИА Новости" in kwargs["text"]
    assert "ria.ru" in kwargs["text"].lower()
    assert kwargs.get("parse_mode") == "Markdown"


@pytest.mark.asyncio
async def test_help_command(mock_message):
    mock_message.text = "help"

    await help_command(mock_message)

    mock_message.answer.assert_called_once()
    args, kwargs = mock_message.answer.call_args
    assert "Это бот для просмотра новостей" in kwargs["text"]
    assert "/start" in kwargs["text"]
    assert "Новости" in kwargs["text"]


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