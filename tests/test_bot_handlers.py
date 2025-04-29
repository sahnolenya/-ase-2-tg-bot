import pytest
from fixtures import mock_

# Когда тест помечен @pytest.mark.asyncio, он становится сопрограммой (coroutine), вместе с ключевым словом await в теле
# pytest выполнит функцию теста как задачу asyncio, используя цикл событий, предоставляемый фикстурой event_loop
# https://habr.com/ru/companies/otus/articles/337108/

@pytest.mark.asyncio
async def test_command_(mock_):
    # # Вызываем хендлер
    # await command_handler(mock_message)

    # # Проверка, что mock_ был вызван
    # assert mock_.called, "message.answer не был вызван"

    # # Проверяем, что mock_ был вызван один раз с ожидаемым результатом
    # mock_.assert_called_once_with(text="Справка!...")

    pass