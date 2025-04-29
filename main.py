# version1.0.0
import asyncio
from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Получаем токен
BOT_TOKEN = os.getenv("BOT_TOKEN")
from handlers import register_message_handlers, set_my_commands

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    register_message_handlers(dp)
    await set_my_commands(bot)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())