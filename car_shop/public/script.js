const tg = window.Telegram.WebApp;
tg.expand();

fetch("/products")
  .then(r => r.json())
  .then(data => {
    const box = document.getElementById("products");

    data.forEach(p => {
      box.innerHTML += `
        <div class="card">
          ${p.media?.endsWith(".mp4")
            ? `<video src="/media/${p.media}" controls></video>`
            : `<img src="/media/${p.media}">`
          }
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
  });

function order(title, price) {
  tg.sendData(JSON.stringify({ title, price }));
  tg.showPopup({
    title: "✅ Заказ отправлен",
    message: "С вами свяжутся в ближайшее время",
    buttons: [{ type: "ok" }]
  });
}
