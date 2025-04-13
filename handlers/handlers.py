
__all__ = ['register_message_handlers']

from aiogram import types, Router, F  # Добавили F
from aiogram.filters import Command
from .keyboard import get_main_keyboard, get_news_keyboard
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def process_start_command(message: types.Message):
    logger.info(f"User {message.from_user.id} started the bot")
    await message.answer(
        "Привет, давай посмотрим новости!",
        reply_markup=get_main_keyboard()
    )

@router.message(F.text == "Новости")
async def handle_news(message: types.Message):
    logger.info(f"User {message.from_user.id} selected 'News'")
    await message.answer(
        "Где вы хотите посмотреть новости?",
        reply_markup=get_news_keyboard()
    )

@router.message(F.text == "Яндекс Дзен")
async def yandex_news(message: types.Message):
    logger.info(f"User {message.from_user.id} selected 'Yandex Zen'")
    await message.answer(
        'Посмотреть новости на сайте: [Яндекс Дзен](https://dzen.ru/?ysclid=m7m6q9lrbo332170005)',
        parse_mode='Markdown'
    )

@router.message(F.text == "Новости РБК")
async def rbc_news(message: types.Message):
    logger.info(f"User {message.from_user.id} selected 'RBC News'")
    await message.answer(
        'Посмотреть новости на сайте: [Новости РБК](https://www.rbc.ru/?ysclid=m7m6pgzzqi625183162)',
        parse_mode='Markdown'
    )

@router.message(F.text == "РИА Новости")
async def ria_news(message: types.Message):
    logger.info(f"User {message.from_user.id} selected 'RIA News'")
    await message.answer(
        'Посмотреть новости на сайте: [РИА Новости](https://ria.ru/?ysclid=m7m6rbckm5753078186)',
        parse_mode='Markdown'
    )

@router.message(F.text == "help")
async def help_command(message: types.Message):
    logger.info(f"User {message.from_user.id} requested help")
    await message.answer("Это бот для просмотра новостей. Доступные команды:\n"
                        "/start - начать работу с ботом\n"
                        "Новости - выбрать источник новостей")

def register_message_handlers(dp):
    dp.include_router(router)