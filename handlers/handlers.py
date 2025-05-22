from aiogram import types, Router, F
from aiogram.filters import Command
from .keyboard import get_main_keyboard, get_news_keyboard, get_role_keyboard, get_confirm_keyboard
from database import Session, User, generate_tutor_code
import logging

logger = logging.getLogger(__name__)
router = Router()

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

# Остальные существующие обработчики
@router.message(F.text == "Новости")
async def handle_news(message: types.Message):
    logger.info(f"User {message.from_user.id} selected 'News'")
    await message.answer(
        "Где вы хотите посмотреть новости?",
19:08


reply_markup=get_news_keyboard()
    )

@router.message(F.text == "Яндекс Дзен")
async def yandex_news(message: types.Message):
    logger.info(f"User {message.from_user.id} selected 'Yandex Zen'")
    await message.answer(
        'Посмотреть новости на сайте: [Яндекс Дзен](https://dzen.ru/)',
        parse_mode='Markdown'
    )

@router.message(F.text == "Новости РБК")
async def rbc_news(message: types.Message):
    logger.info(f"User {message.from_user.id} selected 'RBC News'")
    await message.answer(
        'Посмотреть новости на сайте: [Новости РБК](https://www.rbc.ru/)',
        parse_mode='Markdown'
    )

@router.message(F.text == "РИА Новости")
async def ria_news(message: types.Message):
    logger.info(f"User {message.from_user.id} selected 'RIA News'")
    await message.answer(
        'Посмотреть новости на сайте: [РИА Новости](https://ria.ru/)',
        parse_mode='Markdown'
    )

@router.message(F.text == "help")
async def help_command(message: types.Message):
    logger.info(f"User {message.from_user.id} requested help")
    await message.answer("Это бот для просмотра новостей. Доступные команды:\n"
                         "/start - начать работу с ботом\n"
                         "/status - показать ваш статус\n"
                         "Новости - выбрать источник новостей")

def register_message_handlers(dp):
    dp.include_router(router)