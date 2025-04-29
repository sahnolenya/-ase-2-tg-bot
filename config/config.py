import logging
# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="logs/bot.log",
    filemode="a",
)
logger = logging.getLogger(__name__)