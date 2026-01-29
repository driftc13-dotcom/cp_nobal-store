# ⚡ Быстрый старт для Railway.app

## 📋 Что нужно

1. Аккаунт на https://railway.app (регистрация через GitHub)
2. Аккаунт на https://github.com
3. Токен бота от @BotFather
4. Твой Telegram ID (узнать через @userinfobot)

## 🚀 5 шагов до запуска

### 1️⃣ Создай репозиторий на GitHub

1. Открой https://github.com/new
2. Название: `car-parking-shop`
3. Сделай публичным
4. Нажми "Create repository"

### 2️⃣ Загрузи код

Открой терминал в папке проекта:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/ТВОЙ_USERNAME/car-parking-shop.git
git push -u origin main
```

### 3️⃣ Деплой на Railway

1. Открой https://railway.app/new
2. Нажми "Deploy from GitHub repo"
3. Выбери `car-parking-shop`
4. Подожди пока задеплоится (~2-3 минуты)

### 4️⃣ Настрой переменные окружения

В Railway:
1. Открой свой проект
2. Вкладка "Variables"
3. Добавь:
   - `TOKEN` = твой токен от @BotFather
   - `ADMIN_ID` = твой Telegram ID
   - `ALLOWED_ADMINS` = твой username (без @)
   - `HOST` = 0.0.0.0

4. Нажми "Deploy" (перезапуск)

### 5️⃣ Получи URL и настрой бота

1. В Railway скопируй URL (например: `https://car-parking-shop-production.up.railway.app`)
2. Открой @BotFather в Telegram
3. Отправь `/setmenubutton`
4. Выбери своего бота
5. Отправь: `https://твой-url.up.railway.app/public/shop.html`

## ✅ Готово!

Теперь:
- Открой своего бота в Telegram
- Нажми кнопку меню внизу
- Откроется магазин! 🎉

## 🔗 Полезные ссылки

- Магазин: `https://твой-url.up.railway.app/public/shop.html`
- Админка: `https://твой-url.up.railway.app/public/admin.html`
- API: `https://твой-url.up.railway.app/products`

## 💡 Советы

- Логи смотри в Railway Dashboard → Deployments
- Для обновления: `git push` - Railway автоматически задеплоит
- Бесплатно: 500 часов/месяц (хватит на тестирование)
