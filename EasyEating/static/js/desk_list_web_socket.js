const businessId = "{{ user.business.id }}"; // İşletme ID'si

const businessSocket = new WebSocket(`ws://localhost:8080/ws/business/${businessId}/`);

businessSocket.onerror = function(e) {
    console.error("WebSocket error: ", e);
};

businessSocket.onclose = function(e) {
    console.log("WebSocket connection closed:", e);
    // Yeniden bağlantı kurmak için bir fonksiyon ekleyebilirsiniz
};

businessSocket.onmessage = function(e) {
    try {
        const data = JSON.parse(e.data);

        // Eğer masa tamamlanmışsa ya da logout olduysa
        if (data.desk_data && data.desk_data.status_code == 0) { // Status 1 mesela logout durumu olabilir
            resetDeskToDefault(data.desk_data.desk_id); // Sadece o masayı sıfırla
        }

        if (data.type === 'order_update') {
            // Gelen sipariş güncellemesini masaya göre işleyin
            var deskId = data.desk_id;
            var orderId = data.order_id;
            var status = data.status;
            var totalPrice = data.total_price;
            var items = data.items;

            // Masa listesinde ve modalda gerekli güncellemeleri yapın
            updateOrderList(deskId, orderId, status, totalPrice, items);
        } else {
            console.log("Received:", data)
            updateDeskUI(data.desk_data); // Eğer logout değilse masayı normal şekilde güncelle
        }
    } catch (error) {
        console.error("WebSocket message parsing error:", error);
    }
};



// Fonksiyon: Masa listesi ve modalda güncellemeleri işleme
function updateOrderList(deskId, orderId, status, totalPrice, items) {
    // Masa bilgilerini DOM üzerinde bulup güncelleyin
    var deskElement = document.getElementById("desk_" + deskId);
    if (deskElement) {
        // Sipariş durumu ve toplam fiyatı masa üzerinde göster
        deskElement.querySelector(".status").textContent = status;
        deskElement.querySelector(".total_price").textContent = totalPrice + "₺";

        // Modal'daki öğe bilgilerini güncelleyin
        var modalElement = document.getElementById("orderModal" + deskId);
        if (modalElement) {
            var itemsList = modalElement.querySelector(".items");
            itemsList.innerHTML = ""; // Eski öğeleri temizle

            // Sipariş ürünlerini modal içerisine ekle
            items.forEach(function(item) {
                var itemElement = document.createElement("li");
                itemElement.innerHTML = `
          ${item.produce__name} 
          <span class="badge badge-primary">${item.quantity}</span> 
          - ${item.unit_price}₺`;
                itemsList.appendChild(itemElement);
            });
        }
    }
}

// Masa UI güncelleme fonksiyonu
function updateDeskUI(desk) {
    const deskElement = $(`#desk-${desk.desk_id}`);
    console.log('Updating desk element:', deskElement);

    if (deskElement.length) {
        // Masa başlığını ve sipariş sayısını güncelle
        deskElement.find('.card-title').text(desk.desk_name);
        deskElement.find('.card-text').text(`Toplam ${desk.order_item_count || 0} adet sipariş mevcuttur`);

        // Masa durumu (renkler ve durum bilgisi) güncelleniyor
        const cardClass = desk.status_code == 2 || desk.is_reserve ? 'danger' : 'success';
        deskElement.removeClass('border-success border-danger').addClass(`border-${cardClass}`);
        deskElement.find('.card-body').removeClass('text-success text-danger').addClass(`text-${cardClass}`);
        deskElement.find('.card-footer').removeClass('bg-success bg-danger').addClass(`bg-${cardClass}`);
        deskElement.find('.card-footer span').text(desk.status || "");

        // Siparişleri güncelle
        updateOrderList(desk.order_items || [], deskElement);

        // Masayı en üste taşı
        deskElement.parent().prepend(deskElement); // Bulunan masayı listede en üste taşır
    }
}

function resetDeskToDefault(deskId) {
    const deskElement = $(`#desk-${deskId}`);

    if (deskElement.length) {
        // Masanın durumunu yeşil olarak güncelle
        deskElement.removeClass('border-danger').addClass('border-success');
        deskElement.find('.card-body').removeClass('text-danger').addClass('text-success');
        deskElement.find('.card-footer').removeClass('bg-danger').addClass('bg-success');
        deskElement.find('.card-footer span').text(''); // Durum yazısını sıfırla


        // Sipariş listesini sıfırlayabilirsin (isteğe bağlı)
        deskElement.find('.list-group').empty().append('<li class="list-group-item">Bekleyen sipariş yoktur.</li>');
    }
}



// Sipariş listesini güncelleme fonksiyonu
function updateOrderList(orderItems, deskElement) {
    const orderListElement = deskElement.find('.list-group');
    orderListElement.empty(); // Mevcut listeyi temizle

    if (orderItems.length > 0) {
        // Her sipariş için liste elemanı oluştur
        orderItems.forEach(order => {
                    const orderItemHTML = `
        <li class="list-group-item d-flex justify-content-between align-items-center">
          <div class="d-flex align-items-center">
            <span class="badge bg-primary rounded-pill mx-1">${order.quantity}</span>
            ${order.image ? `<img src="${order.image.url}" alt="${order.product_name}" class="me-3 rounded-circle" style="max-height: 40px; width: 40px;">` : ''}
            <span>${order.product_name}</span>
          </div>
          <button type="button" class="btn btn-outline-primary btn-sm mark-as-served" data-order-item-id="${order.id}" ${order.is_service ? 'disabled' : ''}>Servis Et</button>
        </li>`;
      orderListElement.append(orderItemHTML);
    });
  } else {
    // Bekleyen sipariş yoksa mesaj göster
    orderListElement.append('<li class="list-group-item">Bekleyen sipariş yoktur.</li>');
  }
}