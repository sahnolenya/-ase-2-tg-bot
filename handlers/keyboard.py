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
            [KeyboardButton(text="Яндекс Дзен"), KeyboardButton(text="Новости РБК")],
            [KeyboardButton(text="РИА Новости"), KeyboardButton(text="Международные")],
            [KeyboardButton(text="Обновить"), KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True
    )

def get_categories_keyboard(source: str) -> ReplyKeyboardMarkup:
    categories = {
        "yandex": ["Спорт", "Авто", "Политика"],
        "rbc": ["Спорт", "Авто", "Политика"],
        "ria": ["Спорт", "Авто", "Политика"]
    }
    buttons = [[KeyboardButton(text=cat)] for cat in categories[source]]
    buttons.append([KeyboardButton(text="Назад")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_international_news_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="CNN International")],
            [KeyboardButton(text="Japan News")],
            [KeyboardButton(text="Назад")]
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