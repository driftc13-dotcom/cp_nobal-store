from fastapi import FastAPI, UploadFile, Form, Request, HTTPException
from fastapi.staticfiles import StaticFiles
import json, uuid, shutil
from urllib.parse import parse_qs

app = FastAPI()

app.mount("/public", StaticFiles(directory="public"), name="public")
app.mount("/media", StaticFiles(directory="media"), name="media")

PRODUCTS_FILE = "products.json"
ALLOWED_ADMINS = ["Arizonaa_cpm", "sukunuma"]

def load_products():
    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_products(data):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_username(request: Request):
    init_data = request.headers.get("x-telegram-init-data")
    if not init_data:
        return None

    data = parse_qs(init_data)
    user_data = data.get("user", [None])[0]
    if not user_data:
        return None

    return json.loads(user_data).get("username")

@app.get("/products")
def get_products():
    return load_products()

@app.post("/add-product")
async def add_product(
    request: Request,
    title: str = Form(...),
    price: str = Form(...),
    file: UploadFile = None
):
    if get_username(request) not in ALLOWED_ADMINS:
        raise HTTPException(status_code=403)

    products = load_products()
    filename = None

    if file:
        filename = f"{uuid.uuid4()}_{file.filename}"
        with open(f"media/{filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    products.append({
        "id": str(uuid.uuid4()),
        "title": title,
        "price": price,
        "media": filename
    })

    save_products(products)
    return {"ok": True}

@app.post("/edit-product")
async def edit_product(
    request: Request,
    id: str = Form(...),
    title: str = Form(...),
    price: str = Form(...),
):
    if get_username(request) not in ALLOWED_ADMINS:
        raise HTTPException(status_code=403)

    products = load_products()
    for p in products:
        if p["id"] == id:
            p["title"] = title
            p["price"] = price
            break

    save_products(products)
    return {"ok": True}

@app.post("/delete-product")
async def delete_product(
    request: Request,
    id: str = Form(...)
):
    if get_username(request) not in ALLOWED_ADMINS:
        raise HTTPException(status_code=403)

    products = load_products()
    products = [p for p in products if p["id"] != id]
    save_products(products)
    return {"ok": True}
