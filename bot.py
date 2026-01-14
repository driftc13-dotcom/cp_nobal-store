from aiogram import Bot, Dispatcher, executor, types
import json

TOKEN = "TOKEN"
ADMIN_ID = 123456789

bot = Bot(TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def order(message: types.Message):
    data = json.loads(message.web_app_data.data)

    await bot.send_message(
        ADMIN_ID,
        f"🛒 Заказ\n"
        f"👤 @{message.from_user.username}\n"
        f"📦 {data['title']}\n"
        f"💰 {data['price']}"
    )

    await bot.send_message(
        message.from_user.id,
        "✅ Ваш заказ отправлен!\n"
        "С вами свяжутся в ближайшее время."
    )

executor.start_polling(dp)
