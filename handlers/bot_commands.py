
__all__ = ['set_my_commands']

from aiogram.types import BotCommand

async def set_my_commands(bot):
    commands = [
        BotCommand(command="/start", description="Запуск бота"),
        BotCommand(command="/help", description="Справка"),
        BotCommand(command="/status", description="Ваш статус")
    ]
    await bot.set_my_commands(commands)