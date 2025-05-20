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

    register_message_handlers(dp)
    await set_my_commands(bot)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())