# -*- coding: utf-8 -*-
from aiogram import types, Router, F
from aiogram.filters import Command
from config.config import logger
from .keyboard import (
    get_main_keyboard,
    get_news_keyboard,
    get_categories_keyboard,
    get_international_news_keyboard,
    get_role_keyboard,
    get_confirm_keyboard
)
from script.classes import NewsBotCore
from script.db import generate_tutor_code

router = Router()
bot_core = NewsBotCore()
current_source = None


# Обработчики команд
@router.message(Command("start"))
async def process_start_command(message: types.Message):
    logger.info(f"User {message.from_user.id} started the bot")
    await message.answer(
        "👋 Привет! Кто вы? Преподаватель или слушатель?",
        reply_markup=get_role_keyboard()
    )


@router.message(Command("status"))
async def handle_status(message: types.Message):
    await show_status(message)


@router.message(Command("help"))
async def help_command(message: types.Message):
    await show_help(message)


# Обработчики текстовых кнопок
@router.message(F.text.in_(["🔄 Перезапуск", "Перезапуск"]))
async def handle_restart(message: types.Message):
    await process_start_command(message)


@router.message(F.text.in_(["📊 Мой статус", "Мой статус", "Статус"]))
async def handle_my_status(message: types.Message):
    await show_status(message)


@router.message(F.text.in_(["❓ Помощь", "Помощь"]))
async def handle_help_button(message: types.Message):
    await show_help(message)


# Общие функции
async def show_status(message: types.Message):
    logger.info(f"User {message.from_user.id} checked status")
    user = await bot_core.register_user(
        message.from_user.id,
        message.from_user.username or message.from_user.full_name
    )

    if not user.role:
        await message.answer("❌ Вы не зарегистрированы. Нажмите /start для регистрации.")
        return

    if user.role == "student":
        await message.answer(
            f"👨‍🎓 Ваш статус: Слушатель\n"
            f"🆔 ID: {user.userid}\n"
            f"👤 Имя: {user.username}\n"
            f"👨‍🏫 Преподаватель: {user.subscribe}"
        )
    elif user.role == "teacher":
        students = await bot_core.get_student_count(user.username)
        await message.answer(
            f"👨‍🏫 Ваш статус: Преподаватель\n"
            f"🆔 ID: {user.userid}\n"
            f"👤 Имя: {user.username}\n"
            f"🔑 Код для студентов: {user.tutorcode}\n"
            f"👨‍🎓 Студентов: {students}"
        )


async def show_help(message: types.Message):
    logger.info(f"User {message.from_user.id} requested help")
    help_text = """
📚 Доступные команды:
/start - 🚀 Начать работу
/status - 📊 Ваш статус
/news - 📰 Открыть новости
/cancel - ❌ Отмена действия

📌 Основные функции:
- Для преподавателей: создание кода доступа
- Для студентов: подписка на преподавателя
- Просмотр новостей по категориям
"""
    await message.answer(help_text)


@router.message(F.text == "👨‍🏫 Преподаватель")
async def handle_teacher(message: types.Message):
    logger.info(f"User {message.from_user.id} selected teacher role")
    tutor_code = generate_tutor_code()
    await bot_core.register_user(
        message.from_user.id,
        message.from_user.username or message.from_user.full_name,
        role="teacher",
        tutorcode=tutor_code
    )
    await message.answer(
        f"👨‍🏫 Вы зарегистрированы как преподаватель. Ваш код для студентов: {tutor_code}",
        reply_markup=get_main_keyboard()
    )


@router.message(F.text == "👨‍🎓 Слушатель")
async def handle_student(message: types.Message):
    logger.info(f"User {message.from_user.id} selected student role")
    await message.answer(
        "📝 Введите код преподавателя для подтверждения:",
        reply_markup=get_confirm_keyboard()
    )


@router.message(F.text.regexp(r'^[A-Z0-9]{6}$'))
async def handle_tutor_code(message: types.Message):
    logger.info(f"User {message.from_user.id} entered tutor code")
    teacher = await bot_core.get_teacher_by_code(message.text)

    if teacher:
        await bot_core.register_user(
            message.from_user.id,
            message.from_user.username or message.from_user.full_name,
            role="student",
            subscribe=teacher.username
        )
        await message.answer(
            f"✅ Вы успешно подписаны на преподавателя {teacher.username}!",
            reply_markup=get_main_keyboard()
        )
    else:
        await message.answer(
            "❌ Неверный код преподавателя. Попробуйте еще раз.",
            reply_markup=get_confirm_keyboard()
        )


@router.message(Command("news"))
@router.message(F.text == "📰 Новости")
async def handle_news(message: types.Message):
    logger.info(f"User {message.from_user.id} opened news")
    await message.answer("📰 Выберите источник новостей:", reply_markup=get_news_keyboard())


@router.message(F.text.in_(["Яндекс Дзен", "Новости РБК", "РИА Новости"]))
async def handle_news_source(message: types.Message):
    global current_source
    logger.info(f"User {message.from_user.id} selected {message.text}")
    source_map = {
        "Яндекс Дзен": "yandex",
        "Новости РБК": "rbc",
        "РИА Новости": "ria"
    }
    current_source = source_map[message.text]
    await message.answer(f"📰 Выберите категорию для {message.text}:",
                         reply_markup=get_categories_keyboard(current_source))


@router.message(F.text.in_(["⚽ Спорт", "🏛️ Политика", "🚗 Авто", "🔬 Наука"]))
async def handle_category(message: types.Message):
    global current_source
    logger.info(f"User {message.from_user.id} selected category {message.text}")

    link = bot_core.get_news_link(current_source, message.text)
    if link:
        source_names = {
            "yandex": "Яндекс Дзен",
            "rbc": "РБК",
            "ria": "РИА Новости"
        }
        await message.answer(
            f"📰 {source_names[current_source]} - {message.text}\n🔗 {link}",
            reply_markup=get_main_keyboard()
        )
    else:
        await message.answer("❌ Ссылка не найдена", reply_markup=get_main_keyboard())


@router.message(F.text == "🌍 Международные")
async def handle_international(message: types.Message):
    logger.info(f"User {message.from_user.id} selected international news")
    await message.answer("🌍 Выберите международный источник:", reply_markup=get_international_news_keyboard())


@router.message(F.text == "🌐 CNN International")
async def handle_cnn(message: types.Message):
    logger.info(f"User {message.from_user.id} selected CNN")
    await message.answer("🌐 CNN International News\n🔗 https://edition.cnn.com", reply_markup=get_main_keyboard())


@router.message(F.text == "🗾 Japan News")
async def handle_japan_news(message: types.Message):
    logger.info(f"User {message.from_user.id} selected Japan News")
    await message.answer("🗾 Japan Times News\n🔗 https://www.japantimes.co.jp", reply_markup=get_main_keyboard())


@router.message(F.text == "🔄 Обновить")
async def handle_refresh(message: types.Message):
    logger.info(f"User {message.from_user.id} refreshed news")
    await message.answer("🔄 Новости обновлены!", reply_markup=get_main_keyboard())


@router.message(Command("cancel"))
@router.message(F.text == "🔙 Назад")
async def handle_back(message: types.Message):
    logger.info(f"User {message.from_user.id} went back")
    await message.answer("🔙 Главное меню", reply_markup=get_main_keyboard())


def register_message_handlers(dp):
    dp.include_router(router)