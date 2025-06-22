from aiogram.types import CallbackQuery
from aiogram import F
from config.config import logger
from database import Session, User

async def callback_help(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Это помощь по боту")

async def callback_status(callback: CallbackQuery):
    await callback.answer()
    with Session() as session:
        user = session.get(User, callback.from_user.id)
        if user:
            await callback.message.answer(f"Ваш статус: {user.role}")
        else:
            await callback.message.answer("Вы не зарегистрированы")

async def callback_start(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Бот перезапущен")

async def callback_message(callback: CallbackQuery):
    if callback.data == "help":
        await callback_help(callback)
    elif callback.data == "status":
        await callback_status(callback)
    elif callback.data == "start":
        await callback_start(callback)