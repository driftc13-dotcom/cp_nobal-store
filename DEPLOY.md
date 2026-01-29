# 🚀 Деплой на Railway.app

## Шаг 1: Подготовка

1. Зарегистрируйся на https://railway.app
2. Подключи свой GitHub аккаунт
3. Создай новый репозиторий на GitHub для этого проекта

## Шаг 2: Загрузка кода на GitHub

```bash
# Инициализируй Git репозиторий
git init

# Добавь все файлы
git add .

# Сделай первый коммит
git commit -m "Initial commit: Car Parking Shop"

# Добавь удаленный репозиторий (замени на свой URL)
git remote add origin https://github.com/твой-username/car-parking-shop.git

# Отправь код на GitHub
git push -u origin main
```

## Шаг 3: Деплой на Railway

1. Открой https://railway.app/dashboard
2. Нажми "New Project"
3. Выбери "Deploy from GitHub repo"
4. Выбери свой репозиторий `car-parking-shop`
5. Railway автоматически обнаружит Python проект

## Шаг 4: Настройка переменных окружения

В Railway Dashboard:

1. Открой свой проект
2. Перейди в "Variables"
3. Добавь следующие переменные:

```
TOKEN=твой_токен_бота_от_BotFather
ADMIN_ID=твой_telegram_id
ALLOWED_ADMINS=username1,username2
HOST=0.0.0.0
```

**Важно:** PORT не нужно указывать - Railway автоматически установит его!

## Шаг 5: Получение URL

1. После деплоя Railway даст тебе URL вида: `https://твой-проект.up.railway.app`
2. Скопируй этот URL

## Шаг 6: Настройка Telegram бота

1. Открой @BotFather в Telegram
2. Отправь `/setmenubutton`
3. Выбери своего бота
4. Отправь URL: `https://твой-проект.up.railway.app/public/shop.html`
5. Готово! 🎉

## Шаг 7: Настройка Web App

1. В @BotFather отправь `/newapp`
2. Выбери своего бота
3. Укажи название: "Car Parking Shop"
4. Укажи описание
5. Загрузи иконку (опционально)
6. Укажи URL: `https://твой-проект.up.railway.app/public/shop.html`

## 🔧 Полезные команды

### Просмотр логов
В Railway Dashboard → Deployments → View Logs

### Перезапуск
В Railway Dashboard → Settings → Restart

### Обновление кода
```bash
git add .
git commit -m "Update"
git push
```
Railway автоматически задеплоит новую версию!

## 📊 Мониторинг

- **Логи бота**: Railway Dashboard → Logs
- **Статус сервера**: Открой `https://твой-проект.up.railway.app/products`
- **Админ-панель**: `https://твой-проект.up.railway.app/public/admin.html`

## ⚠️ Важные замечания

1. **Бесплатный план Railway**: 500 часов в месяц (достаточно для тестирования)
2. **Файлы media**: При перезапуске могут удалиться (используй облачное хранилище для продакшена)
3. **products.json**: Также может сброситься (используй базу данных для продакшена)

## 🆙 Апгрейд для продакшена

Для серьезного использования рекомендую:
- Использовать PostgreSQL вместо JSON файла
- Использовать S3/Cloudinary для медиафайлов
- Добавить Redis для кэширования
- Настроить мониторинг и алерты

## 🐛 Решение проблем

**Бот не отвечает:**
- Проверь переменные окружения в Railway
- Проверь логи на наличие ошибок

**Сервер не запускается:**
- Проверь что все зависимости в requirements.txt
- Проверь логи Railway

**403 ошибка в админ-панели:**
- Убедись что твой username в ALLOWED_ADMINS
- Перезапусти проект после изменения переменных
