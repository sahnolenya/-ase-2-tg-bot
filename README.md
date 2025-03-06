# -ase-2-tg-bot
ranepa telegram bot
1 шаг – получили токен бота через BotFather через телеграмм
2 шаг – Создал репозиторий и пригласил участников ( sahnolenya, TEMOCH-KUS, KirShin123, Asker56363636363)
3 шаг – Настроили лицензии в репозитории 
4 – подключил GitHub к PyCharm
5 шаг – Установил нужные пакеты для проекта через Python Packages ( aiogram, Python-dotenv, .env)
6 Шаг – Создали файлы – Main.py, Config.py, .env, requiremets.txt.
7 шаг – написали основной код
8 шаг – за коммитили основу кода и обработчики для кнопок 
Аскер – 

# Обработчик для кнопки "РИА Новости"
@dp.message(F.text == "РИА Новости")
async def ria_news(message: types.Message):
    await message.answer(
        'Посмотреть новости на сайте: [РИА Новости](https://ria.ru/?ysclid=m7m6rbckm5753078186)',
        parse_mode='Markdown'
    )

Артем – 

# Обработчик для кнопки "Новости РБК"
@dp.message(F.text == "Новости РБК")
async def rbc_news(message: types.Message):
    await message.answer(
        'Посмотреть новости на сайте: [Новости РБК](https://www.rbc.ru/?ysclid=m7m6pgzzqi625183162)',
        parse_mode='Markdown'
    )
    
Кирилл – 

# Обработчик для кнопки "Яндекс Дзен"
@dp.message(F.text == "Яндекс Дзен")
async def yandex_news(message: types.Message):
    await message.answer(
        'Посмотреть новости на сайте: [Яндекс Дзен](https://dzen.ru/?ysclid=m7m6q9lrbo332170005)',
        parse_mode='Markdown'
    )

Леня – 

from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram import F
from config.config import BOT_TOKEN  # Импортируем токен из config.py

# Инициализация бота
bot = Bot(token=BOT_TOKEN)

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



9 шаг – Написали код в файл (Config.py)

from dotenv import load_dotenv
from os import getenv

load_dotenv()

TOKEN:str = getenv('TOKEN')

10 шаг – Написали код в файл (.env) - Лежит ТОКЕН бота
11 шаг – Сохранили пакеты, которые используем в проекте в файле (requiremets.txt) через команды ( pip list - pip freeze > requiremets.txt).

﻿aiofiles==24.1.0
aiogram==3.18.0
aiohappyeyeballs==2.4.6
aiohttp==3.11.13
aiosignal==1.3.2
annotated-types==0.7.0
async-timeout==4.0.3
attrs==25.1.0
Babel==2.9.1
certifi==2025.1.31
charset-normalizer==3.4.1
frozenlist==1.5.0
idna==3.10
magic-filter==1.0.12
multidict==6.1.0
propcache==0.3.0
pydantic==2.10.6
pydantic_core==2.27.2
python-dotenv==1.0.1
pytz==2025.1
typing_extensions==4.12.2
yarl==1.18.3

12 шаг – Запустили и проверили код 
14 шаг – исправляли ошибки кода 
15 шаг – Запустили и проверили работоспособность кода.
 
