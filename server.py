from fastapi import FastAPI, UploadFile, Form, Request, HTTPException
from fastapi.staticfiles import StaticFiles
import json, uuid, shutil
from urllib.parse import parse_qs
from services import ProductService, MediaService, AuthService
from config import ALLOWED_ADMINS, HOST, PORT

app = FastAPI()

app.mount("/public", StaticFiles(directory="public"), name="public")
app.mount("/media", StaticFiles(directory="media"), name="media")

def get_username(request: Request):
    init_data = request.headers.get("x-telegram-init-data")
    return AuthService.extract_username(init_data)

def check_admin(request: Request):
    """Проверяет права администратора"""
    username = get_username(request)
    if not AuthService.is_admin(username, ALLOWED_ADMINS):
        raise HTTPException(status_code=403, detail="Доступ запрещен")

@app.get("/products")
def get_products():
    return ProductService.load_products()

@app.post("/add-product")
async def add_product(
    request: Request,
    title: str = Form(...),
    price: str = Form(...),
    file: UploadFile = None
):
    check_admin(request)
    
    # Валидация обязательных полей
    if not title or not title.strip():
        raise HTTPException(status_code=400, detail="Название товара обязательно")
    
    if not price or not price.strip():
        raise HTTPException(status_code=400, detail="Цена товара обязательна")

    products = ProductService.load_products()
    filename = None

    if file:
        filename = MediaService.save_media(file, file.filename)
        if filename is None:
            raise HTTPException(status_code=400, detail="Неподдерживаемый тип файла")

    products.append({
        "id": ProductService.generate_unique_id(),
        "title": title.strip(),
        "price": price.strip(),
        "media": filename
    })

    ProductService.save_products(products)
    return {"ok": True}

@app.post("/edit-product")
async def edit_product(
    request: Request,
    id: str = Form(...),
    title: str = Form(...),
    price: str = Form(...),
):
    check_admin(request)
    
    # Валидация обязательных полей
    if not title or not title.strip():
        raise HTTPException(status_code=400, detail="Название товара обязательно")
    
    if not price or not price.strip():
        raise HTTPException(status_code=400, detail="Цена товара обязательна")

    products = ProductService.load_products()
    product_found = False
    updated_product = None
    
    for p in products:
        if p["id"] == id:
            p["title"] = title.strip()
            p["price"] = price.strip()
            updated_product = p
            product_found = True
            break
    
    if not product_found:
        raise HTTPException(status_code=404, detail="Товар не найден")

    ProductService.save_products(products)
    return {"ok": True, "product": updated_product}

@app.post("/delete-product")
async def delete_product(
    request: Request,
    id: str = Form(...)
):
    check_admin(request)

    products = ProductService.load_products()
    
    # Найти товар для удаления
    product_to_delete = None
    for p in products:
        if p["id"] == id:
            product_to_delete = p
            break
    
    if not product_to_delete:
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    # Удалить медиафайл если есть
    if product_to_delete.get("media"):
        import os
        media_path = os.path.join("media", product_to_delete["media"])
        if os.path.exists(media_path):
            try:
                os.remove(media_path)
            except Exception as e:
                # Логируем ошибку но продолжаем удаление товара
                import logging
                logging.error(f"Не удалось удалить медиафайл {media_path}: {e}")
    
    # Удалить товар из списка
    products = [p for p in products if p["id"] != id]
    ProductService.save_products(products)
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn
    import logging
    import os
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Railway предоставляет PORT через переменную окружения
    port = int(os.getenv("PORT", PORT))
    
    logger.info(f"Запуск FastAPI сервера на {HOST}:{port}")
    uvicorn.run(app, host=HOST, port=port)
