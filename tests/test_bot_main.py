import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import asyncio
from main import main


@pytest.mark.asyncio
async def test_main():
    # Создаём и настраиваем моки
    mock_bot = AsyncMock()
    mock_dispatcher = MagicMock()
    mock_dispatcher.start_polling = AsyncMock()

    # Мок для set_my_commands
    mock_set_commands = AsyncMock()

    with patch('main.Bot', return_value=mock_bot), \
            patch('main.Dispatcher', return_value=mock_dispatcher), \
            patch('main.set_my_commands', mock_set_commands), \
            patch('main.register_message_handlers'):

        # Запускаем main() с таймаутом
        try:
            await asyncio.wait_for(main(), timeout=1.0)
        except asyncio.TimeoutError:
            pass  # Ожидаемое поведение для start_polling

        # Проверяем вызовы
        mock_dispatcher.start_polling.assert_awaited_once_with(mock_bot)
        mock_set_commands.assert_awaited_once_with(mock_bot)