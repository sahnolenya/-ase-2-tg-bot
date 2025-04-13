from aiogram.types import CallbackQuery
from aiogram import F

async def callback_help(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Это помощь по боту")

async def callback_message(callback: CallbackQuery):
    if callback.data == "help":
        await callback_help(callback)
    # Добавьте другие обработчики по аналогии