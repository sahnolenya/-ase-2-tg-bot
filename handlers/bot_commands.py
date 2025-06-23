from aiogram.types import BotCommand

async def set_my_commands(bot):
    """Установка команд меню бота"""
    commands = [
        BotCommand(command="/start", description="Запуск бота"),
        BotCommand(command="/help", description="Справка"),
        BotCommand(command="/status", description="Ваш статус"),
        BotCommand(command="/news", description="Открыть новости"),
        BotCommand(command="/cancel", description="Отмена действия")
    ]
    await bot.set_my_commands(commands)