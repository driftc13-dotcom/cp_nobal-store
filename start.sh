#!/bin/bash

# Скрипт запуска Telegram Shop Mini App

echo "🚀 Запуск Car Parking Shop..."

# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не установлен"
    exit 1
fi

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден"
    echo "Создайте файл .env на основе .env.example:"
    echo "  cp .env.example .env"
    echo "И заполните все необходимые переменные"
    exit 1
fi

# Проверка зависимостей
echo "📦 Проверка зависимостей..."
python3 -m pip install -r requirements.txt --quiet

# Создание необходимых директорий
echo "📁 Создание директорий..."
mkdir -p media
mkdir -p tests

# Инициализация products.json если не существует
if [ ! -f products.json ]; then
    echo "[]" > products.json
    echo "✅ Создан файл products.json"
fi

# Запуск FastAPI сервера в фоне
echo "🌐 Запуск FastAPI сервера..."
python3 server.py &
SERVER_PID=$!
echo "✅ Сервер запущен (PID: $SERVER_PID)"

# Небольшая задержка для запуска сервера
sleep 2

# Запуск Telegram бота
echo "🤖 Запуск Telegram бота..."
python3 bot.py &
BOT_PID=$!
echo "✅ Бот запущен (PID: $BOT_PID)"

echo ""
echo "✨ Приложение успешно запущено!"
echo ""
echo "📊 Процессы:"
echo "  - FastAPI сервер: PID $SERVER_PID"
echo "  - Telegram бот: PID $BOT_PID"
echo ""
echo "🛑 Для остановки нажмите Ctrl+C"
echo ""

# Функция для корректного завершения
cleanup() {
    echo ""
    echo "🛑 Остановка приложения..."
    kill $SERVER_PID 2>/dev/null
    kill $BOT_PID 2>/dev/null
    echo "✅ Приложение остановлено"
    exit 0
}

# Обработка сигнала завершения
trap cleanup SIGINT SIGTERM

# Ожидание завершения процессов
wait
