import os
import json
import asyncio
from aiogram import Bot, Dispatcher, types

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [
    123456789,  # ID Arizonaa_cpm
    987654321,  # ID sukunuma
]

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def order(message: types.Message):
    data = json.loads(message.web_app_data.data)

    text = (
        "🛒 Новый заказ\n"
        f"👤 @{message.from_user.username}\n"
        f"📦 {data['title']}\n"
        f"💰 {data['price']}"
    )

    for admin in ADMIN_IDS:
        await bot.send_message(admin, text)

    await bot.send_message(
        message.from_user.id,
        "✅ Ваш заказ отправлен!\n"
        "С вами свяжутся в ближайшее время."
    )

async def start_bot():
    await dp.start_polling(bot)
