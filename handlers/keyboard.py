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