# version: 0.1.0
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram import F
from config.config import TOKEN # Импортируем токен из config.py

# Инициализация бота
bot = Bot(token=TOKEN)

# Инициализация диспетчера
dp = Dispatcher()


# Обработчик команды /start
@dp.message(Command("start"))
async def start(message: types.Message):
    # Создаем клавиатуру с одной кнопкой "Новости"
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Новости")]  # Список кнопок в одном ряду
        ],
        resize_keyboard=True  # Опционально: автоматическое изменение размера клавиатуры
    )

    await message.answer("Привет, давай посмотрим новости!", reply_markup=markup)


# Обработчик текстовых сообщений
@dp.message(F.text == "Новости")
async def news(message: types.Message):
    # Создаем клавиатуру с кнопками для выбора источника новостей
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Яндекс Дзен")],  # Первый ряд
            [KeyboardButton(text="Новости РБК")],  # Второй ряд
            [KeyboardButton(text="РИА Новости")]   # Третий ряд
        ],
        resize_keyboard=True  # Опционально: автоматическое изменение размера клавиатуры
    )

    await message.answer('Где вы хотите посмотреть новости?', reply_markup=markup)


# Обработчик для кнопки "Яндекс Дзен"
@dp.message(F.text == "Яндекс Дзен")
async def yandex_news(message: types.Message):
    await message.answer(
        'Посмотреть новости на сайте: [Яндекс Дзен](https://dzen.ru/?ysclid=m7m6q9lrbo332170005)',
        parse_mode='Markdown'
    )
# Обработчик для кнопки "Новости РБК"
@dp.message(F.text == "Новости РБК")
async def rbc_news(message: types.Message):
    await message.answer(
        'Посмотреть новости на сайте: [Новости РБК](https://www.rbc.ru/?ysclid=m7m6pgzzqi625183162)',
        parse_mode='Markdown'
    )

# Обработчик для кнопки "РИА Новости"
@dp.message(F.text == "РИА Новости")
async def ria_news(message: types.Message):
    await message.answer(
        'Посмотреть новости на сайте: [РИА Новости](https://ria.ru/?ysclid=m7m6rbckm5753078186)',
        parse_mode='Markdown'
    )


# Запуск бота
if __name__ == '__main__':
    dp.run_polling(bot)  # Запуск бота
