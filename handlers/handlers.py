from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboard import get_main_keyboard, get_news_keyboard, get_role_keyboard, get_confirm_keyboard
from database import Session, User, generate_tutor_code
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime

router = Router()
logger = logging.getLogger(__name__)


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


# Категории для каждого источника
CATEGORIES = {
    "yandex": ["Технологии", "Наука", "Искусство"],
    "rbc": ["Политика", "Экономика", "Технологии"],
    "ria": ["Политика", "Экономика", "Наука"]
}


@router.message(F.text == "Яндекс Дзен")
async def yandex_news(message: types.Message):
    logger.info(f"User {message.from_user.id} selected 'Yandex Zen'")

    builder = InlineKeyboardBuilder()
    for category in CATEGORIES["yandex"]:
        builder.button(text=category, callback_data=f"zen_{category.lower()}")

    builder.adjust(1)
    await message.answer(
        "Выберите категорию новостей Яндекс Дзен:",
        reply_markup=builder.as_markup()
    )


@router.message(F.text == "Новости РБК")
async def rbc_news(message: types.Message):
    logger.info(f"User {message.from_user.id} selected 'RBC News'")

    builder = InlineKeyboardBuilder()
    for category in CATEGORIES["rbc"]:
        builder.button(text=category, callback_data=f"rbc_{category.lower()}")

    builder.adjust(1)
    await message.answer(
        "Выберите категорию новостей РБК:",
        reply_markup=builder.as_markup()
    )


@router.message(F.text == "РИА Новости")
async def ria_news(message: types.Message):
    logger.info(f"User {message.from_user.id} selected 'RIA News'")

    builder = InlineKeyboardBuilder()
    for category in CATEGORIES["ria"]:
        builder.button(text=category, callback_data=f"ria_{category.lower()}")

    builder.adjust(1)
    await message.answer(
        "Выберите категорию новостей РИА Новости:",
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data.startswith(("zen_", "rbc_", "ria_")))
async def process_category(callback: types.CallbackQuery):
    source, category = callback.data.split("_")
    source_name = {
        "zen": "Яндекс Дзен",
        "rbc": "РБК",
        "ria": "РИА Новости"
    }[source]

    await callback.message.edit_text(
        f"Вы выбрали: {source_name} - {category.capitalize()}\n"
        f"Здесь будут новости этой категории..."
    )
    await callback.answer()


# Конфигурация парсеров для каждого источника
NEWS_CONFIG = {
    "rbc": {
        "name": "РБК",
        "categories": {
            "sport": {
                "url": "https://www.rbc.ru/sport/",
                "parser": lambda soup: [
                    (item.find('span', class_='news-feed__item__title').text.strip(),
                     item.find('a')['href'])
                    for item in soup.find_all('div', class_='news-feed__item', limit=3)
                ]
            },
            "auto": {
                "url": "https://www.rbc.ru/auto/",
                "parser": lambda soup: [
                    (item.find('span', class_='news-feed__item__title').text.strip(),
                     item.find('a')['href'])
                    for item in soup.find_all('div', class_='news-feed__item', limit=3)
                ]
            },
            "politics": {
                "url": "https://www.rbc.ru/politics/",
                "parser": lambda soup: [
                    (item.find('span', class_='news-feed__item__title').text.strip(),
                     item.find('a')['href'])
                    for item in soup.find_all('div', class_='news-feed__item', limit=3)
                ]
            }
        }
    },
    "ria": {
        "name": "РИА Новости",
        "categories": {
            "sport": {
                "url": "https://rsport.ria.ru/",
                "parser": lambda soup: [
                    (item.text.strip(),
                     item['href'] if item['href'].startswith('http') else f"https://rsport.ria.ru{item['href']}")
                    for item in soup.find_all('a', class_='list-item__title', limit=3)
                ]
            },
            "auto": {
                "url": "https://ria.ru/transport/",
                "parser": lambda soup: [
                    (item.text.strip(),
                     item['href'] if item['href'].startswith('http') else f"https://ria.ru{item['href']}")
                    for item in soup.find_all('a', class_='list-item__title', limit=3)
                ]
            },
            "politics": {
                "url": "https://ria.ru/politics/",
                "parser": lambda soup: [
                    (item.text.strip(),
                     item['href'] if item['href'].startswith('http') else f"https://ria.ru{item['href']}")
                    for item in soup.find_all('a', class_='list-item__title', limit=3)
                ]
            }
        }
    },
    "zen": {
        "name": "Яндекс Дзен",
        "categories": {
            "sport": {
                "url": "https://zen.yandex.ru/sport",
                "parser": lambda soup: [
                    (item.find('h2').text.strip(),
                     "https://zen.yandex.ru" + item.find('a')['href'])
                    for item in soup.find_all('article', limit=3)
                ]
            },
            "auto": {
                "url": "https://zen.yandex.ru/auto",
                "parser": lambda soup: [
                    (item.find('h2').text.strip(),
                     "https://zen.yandex.ru" + item.find('a')['href'])
                    for item in soup.find_all('article', limit=3)
                ]
            },
            "politics": {
                "url": "https://zen.yandex.ru/politics",
                "parser": lambda soup: [
                    (item.find('h2').text.strip(),
                     "https://zen.yandex.ru" + item.find('a')['href'])
                    for item in soup.find_all('article', limit=3)
                ]
            }
        }
    }
}


# Главное меню
@router.message(Command("start"))
async def start(message: types.Message):
    builder = InlineKeyboardBuilder()
    for source_id, config in NEWS_CONFIG.items():
        builder.add(types.InlineKeyboardButton(
            text=config["name"],
            callback_data=f"source_{source_id}"
        ))
    builder.adjust(1)
    await message.answer(
        "📰 Выберите источник новостей:",
        reply_markup=builder.as_markup()
    )


# Выбор категории
@router.callback_query(F.data.startswith("source_"))
async def select_category(callback: types.CallbackQuery):
    source_id = callback.data.split("_")[1]
    builder = InlineKeyboardBuilder()

    for category_id in NEWS_CONFIG[source_id]["categories"]:
        builder.add(types.InlineKeyboardButton(
            text=category_id.capitalize(),
            callback_data=f"news_{source_id}_{category_id}"
        ))

    builder.adjust(1)
    await callback.message.edit_text(
        f"Выберите категорию в {NEWS_CONFIG[source_id]['name']}:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


# Парсинг и вывод новостей
@router.callback_query(F.data.startswith("news_"))
async def parse_news(callback: types.CallbackQuery):
    _, source_id, category_id = callback.data.split("_")
    config = NEWS_CONFIG[source_id]["categories"][category_id]

    try:
        start_time = datetime.now()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(config["url"], headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        news_items = config["parser"](soup)
        response_text = "\n\n".join(
            [f"📰 {title}\n🔗 {link}" for title, link in news_items]
        )

        parse_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"Parsed {source_id}/{category_id} in {parse_time:.2f}s")

        await callback.message.edit_text(
            f"🔎 {NEWS_CONFIG[source_id]['name']} - {category_id.capitalize()}:\n\n{response_text}"
        )
    except Exception as e:
        logger.error(f"Error parsing {source_id}/{category_id}: {str(e)}")
        await callback.message.edit_text(
            f"⚠ Не удалось загрузить новости. Попробуйте позже.\nОшибка: {str(e)}"
        )

    await callback.answer()


if __name__ == "__main__":
    from aiogram import Dispatcher, Bot
    import asyncio
    from dotenv import load_dotenv
    from os import getenv
    import logging

    # Загрузка переменных окружения
    load_dotenv()

    # Настройка логгирования
    logging.basicConfig(level=logging.INFO)

    # Создание бота с токеном из .env
    bot = Bot(token=getenv("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(router)

    async def main():
        await dp.start_polling(bot)

    asyncio.run(main())


@router.message(F.text == "help")
async def help_command(message: types.Message):
    logger.info(f"User {message.from_user.id} requested help")
    await message.answer("Это бот для просмотра новостей. Доступные команды:\n"
                         "/start - начать работу с ботом\n"
                         "/status - показать ваш статус\n"
                         "Новости - выбрать источник новостей")

def register_message_handlers(dp):
    dp.include_router(router)