from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Новости")],
            [KeyboardButton(text="help")],
            [KeyboardButton(text="status")],
            [KeyboardButton(text="start")]
        ],
        resize_keyboard=True
    )

def get_news_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Яндекс Дзен")],
            [KeyboardButton(text="Новости РБК")],
            [KeyboardButton(text="РИА Новости")]
        ],
        resize_keyboard=True
    )

def get_role_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Преподаватель")],
            [KeyboardButton(text="Слушатель")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_confirm_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отмена")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )