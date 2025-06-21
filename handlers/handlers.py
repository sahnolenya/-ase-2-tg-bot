from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .keyboard import (
    get_main_keyboard,
    get_news_keyboard,
    get_categories_keyboard,
    get_international_news_keyboard,
    get_role_keyboard,
    get_confirm_keyboard
)
from database import Session, User, generate_tutor_code
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime

router = Router()
logger = logging.getLogger(__name__)


# Регистрация пользователя
async def register_user(user_id: int, username: str, role: str = None, tutorcode: str = None, subscribe: str = None):
    with Session() as session:
        user = session.get(User, user_id)
        if not user:
            user = User(
                userid=user_id,
                username=username,
                role=role,
                tutorcode=tutorcode,
                subscribe=subscribe
            )
            session.add(user)
        else:
            user.role = role or user.role
            user.tutorcode = tutorcode or user.tutorcode
            user.subscribe = subscribe or user.subscribe
        session.commit()
        return user


# Обработчики команд
@router.message(Command("start"))
async def process_start_command(message: types.Message):
    logger.info(f"User {message.from_user.id} started the bot")
    await message.answer(
        "Привет! Кто вы? Преподаватель или слушатель?",
        reply_markup=get_role_keyboard()
    )


@router.message(F.text == "Преподаватель")
async def handle_teacher(message: types.Message):
    tutor_code = generate_tutor_code()
    await register_user(
        message.from_user.id,
        message.from_user.username or message.from_user.full_name,
        role="teacher",
        tutorcode=tutor_code
    )
    await message.answer(
        f"Вы зарегистрированы как преподаватель. Ваш код для студентов: {tutor_code}",
        reply_markup=get_main_keyboard()
    )


@router.message(F.text == "Слушатель")
async def handle_student(message: types.Message):
    await message.answer(
        "Введите код преподавателя для подтверждения:",
        reply_markup=get_confirm_keyboard()
    )


@router.message(F.text.regexp(r'^[A-Z0-9]{6}$'))
async def handle_tutor_code(message: types.Message):
    with Session() as session:
        teacher = session.query(User).filter(
            User.tutorcode == message.text,
            User.role == "teacher"
        ).first()

        if teacher:
            await register_user(
                message.from_user.id,
                message.from_user.username or message.from_user.full_name,
                role="student",
                subscribe=teacher.username
            )
            await message.answer(
                f"Вы успешно подписаны на преподавателя {teacher.username}!",
                reply_markup=get_main_keyboard()
            )
        else:
            await message.answer(
                "Неверный код преподавателя. Попробуйте еще раз.",
                reply_markup=get_confirm_keyboard()
            )


@router.message(Command("status"))
async def handle_status(message: types.Message):
    with Session() as session:
        user = session.get(User, message.from_user.id)

        if not user:
            await message.answer(
                "Вы не зарегистрированы. Нажмите /start для регистрации."
            )
            return

        if user.role == "student":
            await message.answer(
                f"Ваш статус: Слушатель\n"
                f"ID: {user.userid}\n"
                f"Имя: {user.username}\n"
                f"Преподаватель: {user.subscribe}"
            )
        elif user.role == "teacher":
            await message.answer(
                f"Ваш статус: Преподаватель\n"
                f"ID: {user.userid}\n"
                f"Имя: {user.username}\n"
                f"Код для студентов: {user.tutorcode}"
            )


# Новостная система
@router.message(F.text == "Новости")
async def handle_news(message: types.Message):
    await message.answer("Выберите источник новостей:", reply_markup=get_news_keyboard())


@router.message(F.text == "Международные")
async def handle_international(message: types.Message):
    await message.answer("Выберите международный источник:", reply_markup=get_international_news_keyboard())


@router.message(F.text == "Обновить")
async def handle_refresh(message: types.Message):
    await message.answer("Новости обновлены!", reply_markup=get_main_keyboard())


@router.message(F.text.in_(["Яндекс Дзен", "Новости РБК", "РИА Новости"]))
async def handle_news_source(message: types.Message):
    source_map = {
        "Яндекс Дзен": "yandex",
        "Новости РБК": "rbc",
        "РИА Новости": "ria"
    }
    source = source_map[message.text]
    await message.answer(f"Выберите категорию для {message.text}:", reply_markup=get_categories_keyboard(source))


@router.message(F.text.in_(["Спорт", "Авто", "Политика"]))
async def handle_category(message: types.Message):
    source = "yandex"  # В реальной реализации это должно быть из состояния
    news_text = await parse_news(source, message.text)
    await message.answer(news_text, reply_markup=get_main_keyboard())


@router.message(F.text == "CNN International")
async def handle_cnn(message: types.Message):
    news_text = await parse_cnn_news()
    await message.answer(news_text, reply_markup=get_main_keyboard())


@router.message(F.text == "Japan News")
async def handle_japan_news(message: types.Message):
    news_text = await parse_japan_news()
    await message.answer(news_text, reply_markup=get_main_keyboard())


@router.message(F.text == "Назад")
async def handle_back(message: types.Message):
    await message.answer("Главное меню", reply_markup=get_main_keyboard())


# Парсеры новостей
async def parse_news(source: str, category: str) -> str:
    url_mapping = {
        "yandex": {
            "Спорт": "https://zen.yandex.ru/sport",
            "Авто": "https://zen.yandex.ru/auto",
            "Политика": "https://zen.yandex.ru/politics"
        },
        "rbc": {
            "Спорт": "https://www.rbc.ru/sport/",
            "Авто": "https://www.rbc.ru/auto/",
            "Политика": "https://www.rbc.ru/politics/"
        },
        "ria": {
            "Спорт": "https://rsport.ria.ru/",
            "Авто": "https://ria.ru/transport/",
            "Политика": "https://ria.ru/politics/"
        }
    }

    url = url_mapping[source][category]
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        news = []
        if source == "yandex":
            items = soup.find_all('article', limit=3)
            for item in items:
                title = item.find('h2').text.strip()
                link = "https://zen.yandex.ru" + item.find('a')['href']
                news.append(f"📰 {title}\n🔗 {link}")
        elif source == "rbc":
            items = soup.find_all('div', class_='news-feed__item', limit=3)
            for item in items:
                title = item.find('span', class_='news-feed__item__title').text.strip()
                link = item.find('a')['href']
                news.append(f"📰 {title}\n🔗 {link}")
        elif source == "ria":
            items = soup.find_all('a', class_='list-item__title', limit=3)
            for item in items:
                title = item.text.strip()
                link = item['href'] if item['href'].startswith('http') else f"https://ria.ru{item['href']}"
                news.append(f"📰 {title}\n🔗 {link}")

        return "\n\n".join(news) if news else "Не удалось найти новости"
    except Exception as e:
        logger.error(f"Ошибка парсинга: {str(e)}")
        return "Ошибка при получении новостей. Попробуйте позже."


async def parse_cnn_news() -> str:
    try:
        url = "https://edition.cnn.com/world"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        news = []
        items = soup.find_all('h3', class_='container__headline', limit=3)
        for item in items:
            title = item.text.strip()
            link = "https://edition.cnn.com" + item.find('a')['href']
            news.append(f"🌐 {title}\n🔗 {link}")

        return "\n\n".join(news) if news else "Не удалось найти новости CNN"
    except Exception as e:
        logger.error(f"Ошибка парсинга CNN: {str(e)}")
        return "Ошибка при получении новостей CNN"


async def parse_japan_news() -> str:
    try:
        url = "https://www.japantimes.co.jp/news/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        news = []
        items = soup.find_all('div', class_='post-style1', limit=3)
        for item in items:
            title = item.find('h2').text.strip()
            link = item.find('a')['href']
            news.append(f"🗾 {title}\n🔗 {link}")

        return "\n\n".join(news) if news else "Не удалось найти новости Japan Times"
    except Exception as e:
        logger.error(f"Ошибка парсинга Japan News: {str(e)}")
        return "Ошибка при получении новостей из Японии"


@router.message(F.text == "help")
async def help_command(message: types.Message):
    logger.info(f"User {message.from_user.id} requested help")
    await message.answer("Это бот для просмотра новостей. Доступные команды:\n"
                         "/start - начать работу с ботом\n"
                         "/status - показать ваш статус\n"
                         "Новости - выбрать источник новостей")


def register_message_handlers(dp):
    dp.include_router(router)