import pytest
from main import main
from fixtures import ,mock_bot, mock_dispatcher, mock_set_my_commands,

@pytest.mark.asyncio
async def test_main(mock_bot, mock_dispatcher, mock_set_my_commands):
    #вызов функции main
    await main()

    #Проверка
    mock_dispatcher.start_polling.assert_awaited_once_with(mock_bot)
    mock_set_my_commands.assert_awaited_once_with(mock_bot())