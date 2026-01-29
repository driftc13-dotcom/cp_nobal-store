const tg = window.Telegram.WebApp;
tg.expand();

const loading = document.getElementById("loading");
const productsBox = document.getElementById("products");

// Показываем индикатор загрузки
loading.style.display = "block";

fetch("/products")
  .then(r => r.json())
  .then(data => {
    // Скрываем индикатор загрузки
    loading.style.display = "none";
    
    // Проверка на пустой каталог
    if (data.length === 0) {
      productsBox.innerHTML = '<div class="empty-message">Товары скоро появятся</div>';
      return;
    }

    data.forEach(p => {
      let mediaHtml = '';
      
      if (p.media) {
        if (p.media.endsWith(".mp4") || p.media.endsWith(".webm") || p.media.endsWith(".mov")) {
          mediaHtml = `<video src="/media/${p.media}" controls></video>`;
        } else {
          mediaHtml = `<img src="/media/${p.media}" onerror="this.src='/public/placeholder.png'; this.onerror=null;">`;
        }
      } else {
        mediaHtml = '<div class="no-media">Нет изображения</div>';
      }
      
      productsBox.innerHTML += `
        <div class="card">
          ${mediaHtml}
          <div class="card-content">
            <h3>${p.title}</h3>
            <p>${p.price}</p>
            <button onclick="order('${p.title}','${p.price}')">
              🛒 Заказать
            </button>
          </div>
        </div>
      `;
    });
  })
  .catch(error => {
    loading.style.display = "none";
    productsBox.innerHTML = '<div class="error-message">Ошибка загрузки товаров. <button onclick="location.reload()">Обновить</button></div>';
    console.error("Ошибка загрузки товаров:", error);
  });

function order(title, price) {
  try {
    tg.sendData(JSON.stringify({ title, price }));
    tg.showPopup({
      title: "✅ Заказ отправлен",
      message: "С вами свяжутся в ближайшее время",
      buttons: [{ type: "ok" }]
    });
  } catch (error) {
    tg.showPopup({
      title: "❌ Ошибка",
      message: "Не удалось отправить заказ. Попробуйте еще раз.",
      buttons: [{ type: "ok" }]
    });
    console.error("Ошибка отправки заказа:", error);
  }
}
