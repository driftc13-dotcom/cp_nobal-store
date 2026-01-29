"""
Скрипт для запуска FastAPI сервера и Telegram бота одновременно на Railway
"""
import subprocess
import sys
import os
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_server():
    """Запускает FastAPI сервер"""
    port = os.getenv("PORT", "8000")
    logger.info(f"Запуск FastAPI сервера на порту {port}")
    return subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "server:app", 
        "--host", "0.0.0.0", 
        "--port", port
    ])

def start_bot():
    """Запускает Telegram бота"""
    logger.info("Запуск Telegram бота")
    return subprocess.Popen([sys.executable, "bot.py"])

if __name__ == "__main__":
    logger.info("🚀 Запуск Car Parking Shop на Railway")
    
    # Запуск сервера
    server_process = start_server()
    time.sleep(2)  # Даем серверу время на запуск
    
    # Запуск бота
    bot_process = start_bot()
    
    logger.info("✅ Оба процесса запущены")
    
    try:
        # Ожидание завершения процессов
        server_process.wait()
        bot_process.wait()
    except KeyboardInterrupt:
        logger.info("🛑 Остановка приложения")
        server_process.terminate()
        bot_process.terminate()
        server_process.wait()
        bot_process.wait()
