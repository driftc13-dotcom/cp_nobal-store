"""
Сервисы для работы с товарами, аутентификацией и медиафайлами
"""
import json
import os
import logging
import uuid
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

PRODUCTS_FILE = "products.json"


class ProductService:
    """Сервис управления товарами"""
    
    @staticmethod
    def generate_unique_id() -> str:
        """
        Генерирует уникальный ID для товара
        
        Returns:
            UUID v4 строка
        """
        return str(uuid.uuid4())
    
    @staticmethod
    def load_products() -> List[Dict]:
        """
        Загружает товары из JSON файла
        
        Returns:
            Список товаров с полями: id, title, price, media
        """
        try:
            # Если файл не существует, создаем пустой
            if not os.path.exists(PRODUCTS_FILE):
                logger.info(f"Файл {PRODUCTS_FILE} не найден, создаем пустой")
                ProductService.save_products([])
                return []
            
            with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
                products = json.load(f)
                
            # Валидация структуры данных
            if not isinstance(products, list):
                logger.error(f"Неверная структура данных в {PRODUCTS_FILE}, ожидается список")
                return []
            
            # Валидация каждого товара
            for product in products:
                if not isinstance(product, dict):
                    logger.warning(f"Пропущен невалидный товар: {product}")
                    continue
                    
                required_fields = ["id", "title", "price"]
                if not all(field in product for field in required_fields):
                    logger.warning(f"Товар не содержит обязательных полей: {product}")
            
            logger.info(f"Загружено {len(products)} товаров")
            return products
            
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка парсинга JSON из {PRODUCTS_FILE}: {e}")
            return []
        except Exception as e:
            logger.error(f"Ошибка при загрузке товаров: {e}")
            return []
    
    @staticmethod
    def save_products(products: List[Dict]) -> bool:
        """
        Сохраняет товары в JSON файл
        
        Args:
            products: Список товаров для сохранения
            
        Returns:
            True если сохранено успешно, False в случае ошибки
        """
        try:
            with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
                json.dump(products, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Сохранено {len(products)} товаров")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при сохранении товаров: {e}")
            return False
    
    @staticmethod
    def get_product_by_id(product_id: str) -> Optional[Dict]:
        """
        Находит товар по ID
        
        Args:
            product_id: ID товара
            
        Returns:
            Товар или None если не найден
        """
        products = ProductService.load_products()
        for product in products:
            if product.get("id") == product_id:
                return product
        return None



class MediaService:
    """Сервис работы с медиафайлами"""
    
    ALLOWED_IMAGE_TYPES = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    ALLOWED_VIDEO_TYPES = {".mp4", ".webm", ".mov"}
    MEDIA_DIR = "media"
    
    @staticmethod
    def save_media(file, filename: str) -> Optional[str]:
        """
        Сохраняет медиафайл с уникальным именем
        
        Args:
            file: Загруженный файл
            filename: Оригинальное имя файла
            
        Returns:
            Имя сохраненного файла или None в случае ошибки
        """
        try:
            # Проверка типа файла
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext not in MediaService.ALLOWED_IMAGE_TYPES and file_ext not in MediaService.ALLOWED_VIDEO_TYPES:
                logger.warning(f"Неподдерживаемый тип файла: {file_ext}")
                return None
            
            # Генерация уникального имени
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            filepath = os.path.join(MediaService.MEDIA_DIR, unique_filename)
            
            # Создание директории если не существует
            os.makedirs(MediaService.MEDIA_DIR, exist_ok=True)
            
            # Сохранение файла
            with open(filepath, "wb") as buffer:
                if hasattr(file, 'file'):
                    # FastAPI UploadFile
                    import shutil
                    shutil.copyfileobj(file.file, buffer)
                else:
                    # Обычный файл
                    buffer.write(file.read())
            
            logger.info(f"Медиафайл сохранен: {unique_filename}")
            return unique_filename
            
        except Exception as e:
            logger.error(f"Ошибка при сохранении медиафайла: {e}")
            return None
    
    @staticmethod
    def is_valid_media_type(filename: str) -> bool:
        """
        Проверяет является ли файл допустимым медиафайлом
        
        Args:
            filename: Имя файла
            
        Returns:
            True если тип файла допустим
        """
        file_ext = os.path.splitext(filename)[1].lower()
        return file_ext in MediaService.ALLOWED_IMAGE_TYPES or file_ext in MediaService.ALLOWED_VIDEO_TYPES



class AuthService:
    """Сервис аутентификации через Telegram"""
    
    @staticmethod
    def extract_username(init_data: str) -> Optional[str]:
        """
        Извлекает username из Telegram init data
        
        Args:
            init_data: Строка из заголовка x-telegram-init-data
            
        Returns:
            Username пользователя или None
        """
        if not init_data:
            logger.warning("Отсутствуют данные x-telegram-init-data")
            return None
        
        try:
            from urllib.parse import parse_qs
            
            data = parse_qs(init_data)
            user_data = data.get("user", [None])[0]
            
            if not user_data:
                logger.warning("Отсутствуют данные пользователя в init_data")
                return None
            
            user_json = json.loads(user_data)
            username = user_json.get("username")
            
            if username:
                logger.info(f"Извлечен username: {username}")
            else:
                logger.warning("Username отсутствует в данных пользователя")
            
            return username
            
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка парсинга JSON из user data: {e}")
            return None
        except Exception as e:
            logger.error(f"Ошибка при извлечении username: {e}")
            return None
    
    @staticmethod
    def is_admin(username: str, allowed_admins: List[str]) -> bool:
        """
        Проверяет является ли пользователь администратором
        
        Args:
            username: Username пользователя
            allowed_admins: Список разрешенных администраторов
            
        Returns:
            True если пользователь в списке администраторов
        """
        if not username:
            logger.info("Попытка проверки прав без username")
            return False
        
        is_admin = username in allowed_admins
        
        if is_admin:
            logger.info(f"Пользователь {username} является администратором")
        else:
            logger.warning(f"Пользователь {username} не является администратором")
        
        return is_admin
