from .handlers import register_message_handlers
from .bot_commands import set_my_commands
from .callbacks import callback_message
from .keyboard import get_main_keyboard, get_news_keyboard

__all__ = [
    'register_message_handlers',
    'set_my_commands',
    'callback_message',
    'get_main_keyboard',
    'get_news_keyboard'
]