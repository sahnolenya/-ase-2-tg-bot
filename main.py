
# version1.0.0
import asyncio
import logging
from aiogram import Bot, Dispatcher
from config.config import BOT_TOKEN
from handlers import register_message_handlers, set_my_commands

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="bot.log",
    filemode="a",
)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    register_message_handlers(dp)
    await set_my_commands(bot)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())