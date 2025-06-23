#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from script.classes import BotLogic
from config.config import logger

# Настройка базового логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def setup_bot_commands(bot: Bot):
    from aiogram.types import BotCommand
    commands = [
        BotCommand(command="/start", description="Запуск бота"),
        BotCommand(command="/help", description="Справка"),
        BotCommand(command="/status", description="Ваш статус"),
        BotCommand(command="/news", description="Открыть новости"),
        BotCommand(command="/cancel", description="Отмена действия")
    ]
    await bot.set_my_commands(commands)


async def main():
    try:
        # Загрузка переменных окружения
        load_dotenv()
        bot_token = os.getenv("BOT_TOKEN")

        if not bot_token:
            raise ValueError("Токен бота не найден в .env файле")

        # Инициализация бота
        bot = Bot(token=bot_token)
        dp = Dispatcher()

        # Инициализация бизнес-логики
        bot_logic = BotLogic(bot)

        # Настройка команд бота
        await setup_bot_commands(bot)

        # Регистрация обработчиков
        bot_logic.register_handlers()
        dp.include_router(bot_logic.router)

        logger.info("Бот успешно запущен")
        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f"Ошибка при работе бота: {e}", exc_info=True)
    finally:
        if 'bot' in locals():
            await bot.session.close()
        logger.info("Работа бота завершена")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
        raise