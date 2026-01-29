"""
Конфигурация приложения из переменных окружения
"""
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Telegram Bot Configuration
TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
ALLOWED_ADMINS = os.getenv("ALLOWED_ADMINS", "").split(",")

# FastAPI Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# Валидация обязательных переменных
def validate_config():
    """Проверяет наличие всех обязательных переменных окружения"""
    errors = []
    
    if not TOKEN:
        errors.append("TOKEN не установлен")
    
    if not ADMIN_ID:
        errors.append("ADMIN_ID не установлен")
    
    if not ALLOWED_ADMINS or ALLOWED_ADMINS == [""]:
        errors.append("ALLOWED_ADMINS не установлен")
    
    if errors:
        error_message = "Ошибки конфигурации:\n" + "\n".join(f"- {e}" for e in errors)
        error_message += "\n\nСоздайте файл .env на основе .env.example и заполните все переменные."
        raise ValueError(error_message)

# Проверка конфигурации при импорте
validate_config()
