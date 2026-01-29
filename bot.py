from aiogram import Bot, Dispatcher, executor, types
import json
import logging
import os
from dotenv import load_dotenv
from bot_services import OrderHandler

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

if not TOKEN:
    raise ValueError("TOKEN не установлен в .env файле")

bot = Bot(TOKEN)
dp = Dispatcher(bot)

# Инициализация обработчика заказов
order_handler = OrderHandler(bot, ADMIN_ID)

@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def order(message: types.Message):
    await order_handler.handle_web_app_data(message)

if __name__ == "__main__":
    logger.info("Запуск бота...")
    executor.start_polling(dp)
