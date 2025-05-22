import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, User, Session
import asyncio

from handlers.handlers import (
    process_start_command,
    handle_news,
    yandex_news,
    rbc_news,
    ria_news,
    help_command,
    register_message_handlers,
    handle_teacher,
    handle_student,
    handle_status,
    handle_tutor_code
)
from handlers.keyboard import get_role_keyboard, get_confirm_keyboard, get_main_keyboard, get_news_keyboard


# Фикстура для тестовой базы данных в памяти
@pytest.fixture(scope="module")
def engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


# Фикстура для сессии с откатом изменений после теста
@pytest.fixture
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    # Подменяем глобальную сессию
    global Session
    Session = sessionmaker(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def mock_message():
    mock = AsyncMock(spec=Message)
    mock.answer = AsyncMock(return_value=None)
    mock.from_user = MagicMock()
    mock.from_user.id = 123
    mock.from_user.username = "test_user"
    mock.from_user.full_name = "Test User"
    mock.text = ""
    return mock


@pytest.fixture
def mock_callback():
    mock = AsyncMock(spec=CallbackQuery)
    mock.message = AsyncMock(spec=Message)
    mock.message.answer = AsyncMock(return_value=None)
    mock.data = ""
    mock.answer = AsyncMock(return_value=None)
    return mock


@pytest.fixture
def mock_dispatcher():
    mock = MagicMock()
    mock.include_router = MagicMock()
    return mock


# Тесты
@pytest.mark.asyncio
async def test_process_start_command(mock_message):
    mock_message.text = "/start"
    await process_start_command(mock_message)
    mock_message.answer.assert_called_once()
    args = mock_message.answer.call_args[0]
    assert "Кто вы? Преподаватель или слушатель?" in args[0]


@pytest.mark.asyncio
async def test_handle_teacher(mock_message, db_session):
    mock_message.text = "Преподаватель"
    await handle_teacher(mock_message)

    mock_message.answer.assert_called_once()
    args = mock_message.answer.call_args[0]
    assert "Вы зарегистрированы как преподаватель" in args[0]

    # Проверяем, что пользователь сохранился в БД
    db_session.commit()  # Явно фиксируем изменения
    user = db_session.query(User).filter_by(userid=mock_message.from_user.id).first()
    assert user is not None
    assert user.role == "teacher"


@pytest.mark.asyncio
async def test_handle_student(mock_message):
    mock_message.text = "Слушатель"
    await handle_student(mock_message)
    mock_message.answer.assert_called_once_with(
        "Введите код преподавателя для подтверждения:",
        reply_markup=get_confirm_keyboard()
    )


@pytest.mark.asyncio
async def test_handle_tutor_code_success(mock_message, db_session):
    # Создаем преподавателя в БД
    teacher = User(
        userid=111,
        username="teacher_user",
        role="teacher",
        tutorcode="ABCDEF"
    )
    db_session.add(teacher)
    db_session.commit()

    # Настраиваем мок для студента
    mock_message.from_user.id = 222
    mock_message.text = "ABCDEF"

    await handle_tutor_code(mock_message)

    mock_message.answer.assert_called_once()
    args = mock_message.answer.call_args[0]
    assert "Вы успешно подписаны на преподавателя teacher_user" in args[0]

    # Проверяем запись студента в БД
    student = db_session.query(User).filter_by(userid=222).first()
    assert student is not None
    assert student.role == "student"


@pytest.mark.asyncio
async def test_handle_tutor_code_failure(mock_message):
    mock_message.text = "INVALID"
    await handle_tutor_code(mock_message)
    mock_message.answer.assert_called_once_with(
        "Неверный код преподавателя. Попробуйте еще раз.",
        reply_markup=get_confirm_keyboard()
    )


@pytest.mark.asyncio
async def test_handle_status_teacher(mock_message, db_session):
    # Создаем преподавателя в БД
    teacher = User(
        userid=mock_message.from_user.id,
        username="test_teacher",
        role="teacher",
        tutorcode="TEST123"
    )
    db_session.add(teacher)
    db_session.commit()

    await handle_status(mock_message)
    mock_message.answer.assert_called_once()
    args = mock_message.answer.call_args[0]
    assert "Преподаватель" in args[0]
    assert "TEST123" in args[0]


@pytest.mark.asyncio
async def test_handle_status_student(db_session):
    # Создаем отдельный мок для студента
    mock_msg = AsyncMock(spec=Message)
    mock_msg.answer = AsyncMock(return_value=None)
    mock_msg.from_user = MagicMock()
    mock_msg.from_user.id = 333
    mock_msg.from_user.username = "test_student"

    # Создаем студента в БД
    student = User(
        userid=333,
        username="test_student",
        role="student",
        subscribe="teacher_name"
    )
    db_session.add(student)
    db_session.commit()

    await handle_status(mock_msg)
    mock_msg.answer.assert_called_once()
    args = mock_msg.answer.call_args[0]
    assert "Слушатель" in args[0]
    assert "teacher_name" in args[0]


@pytest.mark.asyncio
async def test_handle_status_unregistered(mock_message):
    mock_message.from_user.id = 999
    await handle_status(mock_message)
    mock_message.answer.assert_called_once_with(
        "Вы не зарегистрированы. Нажмите /start для регистрации."
    )


# Остальные тесты без изменений
@pytest.mark.asyncio
async def test_handle_news(mock_message):
    mock_message.text = "Новости"
    await handle_news(mock_message)
    mock_message.answer.assert_called_once()
    args = mock_message.answer.call_args[0]
    assert "Где вы хотите посмотреть новости?" in args[0]


@pytest.mark.asyncio
async def test_yandex_news(mock_message):
    mock_message.text = "Яндекс Дзен"
    await yandex_news(mock_message)
    mock_message.answer.assert_called_once()
    args = mock_message.answer.call_args[0]
    assert "Яндекс Дзен" in args[0]


@pytest.mark.asyncio
async def test_rbc_news(mock_message):
    mock_message.text = "Новости РБК"
    await rbc_news(mock_message)
    mock_message.answer.assert_called_once()
    args = mock_message.answer.call_args[0]
    assert "РБК" in args[0]


@pytest.mark.asyncio
async def test_ria_news(mock_message):
    mock_message.text = "РИА Новости"
    await ria_news(mock_message)
    mock_message.answer.assert_called_once()
    args = mock_message.answer.call_args[0]
    assert "РИА Новости" in args[0]


@pytest.mark.asyncio
async def test_help_command(mock_message):
    mock_message.text = "help"
    await help_command(mock_message)
    mock_message.answer.assert_called_once()
    args = mock_message.answer.call_args[0]
    assert "Это бот для просмотра новостей" in args[0]


@pytest.mark.asyncio
async def test_register_message_handlers(mock_dispatcher):
    register_message_handlers(mock_dispatcher)
    mock_dispatcher.include_router.assert_called_once()