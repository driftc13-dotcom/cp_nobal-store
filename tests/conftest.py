"""
Общие фикстуры для тестов
"""
import pytest
import json
import os
from pathlib import Path

@pytest.fixture
def temp_products_file(tmp_path):
    """Создает временный файл products.json для тестов"""
    products_file = tmp_path / "products.json"
    products_file.write_text("[]", encoding="utf-8")
    return products_file

@pytest.fixture
def sample_product():
    """Возвращает пример товара"""
    return {
        "id": "test-uuid-123",
        "title": "Тестовый товар",
        "price": "1000₽",
        "media": "test.jpg"
    }

@pytest.fixture
def sample_products():
    """Возвращает список примеров товаров"""
    return [
        {
            "id": "uuid-1",
            "title": "Товар 1",
            "price": "100₽",
            "media": "image1.jpg"
        },
        {
            "id": "uuid-2",
            "title": "Товар 2",
            "price": "200₽",
            "media": "video2.mp4"
        },
        {
            "id": "uuid-3",
            "title": "Товар 3",
            "price": "300₽",
            "media": None
        }
    ]
