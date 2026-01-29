"""
Сервисы для Telegram бота
"""
import json
import logging
from typing import Dict, Optional
from aiogram import Bot, types

logger = logging.getLogger(__name__)


class OrderHandler:
    """Обработчик заказов от WebApp"""
    
    def __init__(self, bot: Bot, admin_id: int):
        self.bot = bot
        self.admin_id = admin_id
        self.notification_service = NotificationService(bot, admin_id)
    
    async def handle_web_app_data(self, message: types.Message) -> None:
        """
        Обрабатывает данные заказа из мини-приложения
        
        Args:
            message: Сообщение с данными WebApp
        """
        try:
            # Валидация данных
            if not message.web_app_data or not message.web_app_data.data:
                logger.error("Отсутствуют данные WebApp")
                await message.answer("❌ Ошибка: данные заказа не получены")
                return
            
            # Парсинг JSON
            try:
                order_data = json.loads(message.web_app_data.data)
            except json.JSONDecodeError as e:
                logger.error(f"Ошибка парсинга JSON заказа: {e}")
                await message.answer("❌ Ошибка: неверный формат данных")
                return
            
            # Валидация полей заказа
            if not order_data.get("title") or not order_data.get("price"):
                logger.error(f"Неполные данные заказа: {order_data}")
                await message.answer("❌ Ошибка: неполные данные заказа")
                return
            
            # Информация о пользователе
            user_info = {
                "id": message.from_user.id,
                "username": message.from_user.username,
                "first_name": message.from_user.first_name
            }
            
            # Отправка уведомлений
            admin_sent = await self.notification_service.notify_admin(order_data, user_info)
            customer_sent = await self.notification_service.confirm_order(message.from_user.id)
            
            if not admin_sent:
                logger.warning("Не удалось отправить уведомление администратору")
            
            if not customer_sent:
                logger.error("Не удалось отправить подтверждение покупателю")
                await message.answer("❌ Ошибка при отправке подтверждения")
            
            logger.info(f"Заказ обработан: {order_data['title']} от @{user_info['username']}")
            
        except Exception as e:
            logger.error(f"Ошибка при обработке заказа: {e}")
            await message.answer("❌ Произошла ошибка при обработке заказа")


class NotificationService:
    """Сервис отправки уведомлений"""
    
    def __init__(self, bot: Bot, admin_id: int):
        self.bot = bot
        self.admin_id = admin_id
    
    async def notify_admin(self, order_data: Dict, user_info: Dict) -> bool:
        """
        Отправляет уведомление администратору о новом заказе
        
        Args:
            order_data: Данные заказа (title, price)
            user_info: Информация о пользователе (username, id, first_name)
            
        Returns:
            True если отправлено успешно
        """
        try:
            username = user_info.get("username")
            user_mention = f"@{username}" if username else user_info.get("first_name", "Пользователь")
            
            message = (
                f"🛒 Новый заказ\n"
                f"👤 {user_mention}\n"
                f"📦 {order_data['title']}\n"
                f"💰 {order_data['price']}"
            )
            
            await self.bot.send_message(self.admin_id, message)
            logger.info(f"Уведомление администратору отправлено")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при отправке уведомления администратору: {e}")
            return False
    
    async def confirm_order(self, user_id: int) -> bool:
        """
        Отправляет подтверждение заказа покупателю
        
        Args:
            user_id: ID пользователя Telegram
            
        Returns:
            True если отправлено успешно
        """
        try:
            message = (
                "✅ Ваш заказ отправлен!\n"
                "С вами свяжутся в ближайшее время."
            )
            
            await self.bot.send_message(user_id, message)
            logger.info(f"Подтверждение покупателю {user_id} отправлено")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при отправке подтверждения покупателю: {e}")
            return False
