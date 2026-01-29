/**
 * Административная панель для управления товарами
 */

const tg = window.Telegram.WebApp;
tg.expand();

const loading = document.getElementById("loading");
const listBox = document.getElementById("list");
const addForm = document.getElementById("addForm");
const addStatus = document.getElementById("addStatus");
const editModal = document.getElementById("editModal");
const editForm = document.getElementById("editForm");
const editStatus = document.getElementById("editStatus");

class AdminPanel {
    constructor() {
        this.products = [];
        this.init();
    }

    init() {
        // Загрузка товаров
        this.loadProducts();
        
        // Обработчики форм
        addForm.addEventListener("submit", (e) => this.handleAddProduct(e));
        editForm.addEventListener("submit", (e) => this.handleEditProduct(e));
        
        // Закрытие модального окна
        document.querySelector(".close").addEventListener("click", () => this.closeModal());
        window.addEventListener("click", (e) => {
            if (e.target === editModal) {
                this.closeModal();
            }
        });
    }

    async loadProducts() {
        try {
            loading.style.display = "block";
            
            const response = await fetch("/products");
            if (!response.ok) {
                throw new Error("Ошибка загрузки товаров");
            }
            
            this.products = await response.json();
            this.renderProducts();
            
        } catch (error) {
            console.error("Ошибка загрузки товаров:", error);
            listBox.innerHTML = '<div class="error-message">Ошибка загрузки товаров</div>';
        } finally {
            loading.style.display = "none";
        }
    }

    renderProducts() {
        if (this.products.length === 0) {
            listBox.innerHTML = '<div class="empty-message">Товары отсутствуют</div>';
            return;
        }

        listBox.innerHTML = "";
        
        this.products.forEach(product => {
            const card = document.createElement("div");
            card.className = "card product-card";
            
            let mediaHtml = "";
            if (product.media) {
                if (product.media.endsWith(".mp4") || product.media.endsWith(".webm")) {
                    mediaHtml = `<video src="/media/${product.media}" controls class="product-media"></video>`;
                } else {
                    mediaHtml = `<img src="/media/${product.media}" class="product-media">`;
                }
            }
            
            card.innerHTML = `
                ${mediaHtml}
                <div class="product-info">
                    <h4>${product.title}</h4>
                    <p class="price">${product.price}</p>
                    <p class="product-id">ID: ${product.id}</p>
                </div>
                <div class="product-actions">
                    <button class="btn-edit" onclick="adminPanel.showEditForm('${product.id}')">
                        ✏️ Редактировать
                    </button>
                    <button class="btn-delete" onclick="adminPanel.deleteProduct('${product.id}')">
                        ❌ Удалить
                    </button>
                </div>
            `;
            
            listBox.appendChild(card);
        });
    }

    async handleAddProduct(e) {
        e.preventDefault();
        
        const title = document.getElementById("newTitle").value.trim();
        const price = document.getElementById("newPrice").value.trim();
        const file = document.getElementById("newFile").files[0];
        
        if (!title || !price) {
            this.showStatus(addStatus, "Заполните все обязательные поля", "error");
            return;
        }
        
        try {
            const formData = new FormData();
            formData.append("title", title);
            formData.append("price", price);
            if (file) {
                formData.append("file", file);
            }
            
            const response = await fetch("/add-product", {
                method: "POST",
                headers: {
                    "x-telegram-init-data": tg.initData
                },
                body: formData
            });
            
            if (response.status === 403) {
                this.showStatus(addStatus, "Доступ запрещен. Вы не являетесь администратором.", "error");
                return;
            }
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || "Ошибка добавления товара");
            }
            
            this.showStatus(addStatus, "Товар успешно добавлен!", "success");
            addForm.reset();
            
            // Обновить список товаров
            await this.loadProducts();
            
        } catch (error) {
            console.error("Ошибка добавления товара:", error);
            this.showStatus(addStatus, error.message, "error");
        }
    }

    showEditForm(productId) {
        const product = this.products.find(p => p.id === productId);
        if (!product) return;
        
        document.getElementById("editId").value = product.id;
        document.getElementById("editTitle").value = product.title;
        document.getElementById("editPrice").value = product.price;
        
        editModal.style.display = "block";
    }

    closeModal() {
        editModal.style.display = "none";
        editForm.reset();
        editStatus.textContent = "";
    }

    async handleEditProduct(e) {
        e.preventDefault();
        
        const id = document.getElementById("editId").value;
        const title = document.getElementById("editTitle").value.trim();
        const price = document.getElementById("editPrice").value.trim();
        
        if (!title || !price) {
            this.showStatus(editStatus, "Заполните все поля", "error");
            return;
        }
        
        try {
            const formData = new FormData();
            formData.append("id", id);
            formData.append("title", title);
            formData.append("price", price);
            
            const response = await fetch("/edit-product", {
                method: "POST",
                headers: {
                    "x-telegram-init-data": tg.initData
                },
                body: formData
            });
            
            if (response.status === 403) {
                this.showStatus(editStatus, "Доступ запрещен", "error");
                return;
            }
            
            if (response.status === 404) {
                this.showStatus(editStatus, "Товар не найден", "error");
                return;
            }
            
            if (!response.ok) {
                throw new Error("Ошибка редактирования товара");
            }
            
            this.showStatus(editStatus, "Товар успешно обновлен!", "success");
            
            // Обновить список товаров
            await this.loadProducts();
            
            // Закрыть модальное окно через 1 секунду
            setTimeout(() => this.closeModal(), 1000);
            
        } catch (error) {
            console.error("Ошибка редактирования товара:", error);
            this.showStatus(editStatus, error.message, "error");
        }
    }

    async deleteProduct(productId) {
        const product = this.products.find(p => p.id === productId);
        if (!product) return;
        
        if (!confirm(`Удалить товар "${product.title}"?`)) {
            return;
        }
        
        try {
            const formData = new FormData();
            formData.append("id", productId);
            
            const response = await fetch("/delete-product", {
                method: "POST",
                headers: {
                    "x-telegram-init-data": tg.initData
                },
                body: formData
            });
            
            if (response.status === 403) {
                alert("Доступ запрещен");
                return;
            }
            
            if (response.status === 404) {
                alert("Товар не найден");
                return;
            }
            
            if (!response.ok) {
                throw new Error("Ошибка удаления товара");
            }
            
            // Обновить список товаров
            await this.loadProducts();
            
        } catch (error) {
            console.error("Ошибка удаления товара:", error);
            alert("Ошибка удаления товара: " + error.message);
        }
    }

    showStatus(element, message, type) {
        element.textContent = message;
        element.className = `status-message ${type}`;
        
        // Очистить через 5 секунд
        setTimeout(() => {
            element.textContent = "";
            element.className = "status-message";
        }, 5000);
    }
}

// Инициализация админ-панели
const adminPanel = new AdminPanel();
