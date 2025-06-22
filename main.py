# -*- coding: utf-8 -*-
import asyncio
from aiogram import Bot, Dispatcher
from handlers.bot_commands import set_my_commands
from handlers.handlers import register_message_handlers
import os
from dotenv import load_dotenv

load_dotenv()


async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    # Устанавливаем команды бота
    await set_my_commands(bot)

    # Регистрируем обработчики
    register_message_handlers(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())