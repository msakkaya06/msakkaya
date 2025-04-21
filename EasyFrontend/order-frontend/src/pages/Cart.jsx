import axios from "axios";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const Cart = () => {
  const [pendingItems, setPendingItems] = useState([]);
  const [confirmedItems, setConfirmedItems] = useState([]);
  const [cartId, setCartId] = useState(null);
  const [totalPrice, setTotalPrice] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");

    axios
      .get(`${process.env.REACT_APP_API_BASE_URL}/order/api/cart/`, {
        headers: {
          Authorization: `Token ${token}`,
        },
      })
      .then((res) => {
        setPendingItems(res.data.pending_items);
        setConfirmedItems(res.data.confirmed_items);
        setCartId(res.data.cart_id);
        setTotalPrice(res.data.total_price);
      })
      .catch((err) => console.error("Sepet verisi alınamadı:", err));
  }, []);

  const handleConfirmOrder = () => {
    const token = localStorage.getItem("token");

    axios
      .post(`${process.env.REACT_APP_API_BASE_URL}/order/api/cart/${cartId}/to-order/`, {}, {
        headers: {
          Authorization: `Token ${token}`,
        },
      })
      .then((res) => {
        alert("Siparişiniz başarıyla oluşturuldu!");
        navigate("/"); // Anasayfaya yönlendir
      })
      .catch((err) => {
        console.error("Sipariş onayı başarısız:", err);
        alert("Sipariş onaylanamadı.");
      });
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Sepet</h1>

      <h2 className="text-xl font-semibold mt-4 mb-2">🕐 Bekleyen Ürünler</h2>
      {pendingItems.length === 0 ? (
        <p className="text-gray-600">Onay bekleyen ürün yok.</p>
      ) : (
        pendingItems.map((item) => (
          <div key={item.id} className="border rounded p-2 mb-2 bg-yellow-50">
            <p><strong>{item.produce.name}</strong></p>
            <p>Adet: {item.quantity}</p>
            <p>Birim Fiyat: {item.unit_price} ₺</p>
          </div>
        ))
      )}

      <h2 className="text-xl font-semibold mt-6 mb-2">✅ Onaylanmış Ürünler</h2>
      {confirmedItems.length === 0 ? (
        <p className="text-gray-600">Onaylanmış ürün bulunmamaktadır.</p>
      ) : (
        confirmedItems.map((item) => (
          <div key={item.id} className="border rounded p-2 mb-2 bg-green-50">
            <p><strong>{item.produce.name}</strong></p>
            <p>Adet: {item.quantity}</p>
            <p>Birim Fiyat: {item.unit_price} ₺</p>
          </div>
        ))
      )}

      <div className="mt-6 text-right font-semibold text-lg">
        Toplam Tutar: {totalPrice} ₺
      </div>

      {pendingItems.length > 0 && (
        <button
          onClick={handleConfirmOrder}
          className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mt-4"
        >
          Siparişi Onayla
        </button>
      )}
    </div>
  );
};

export default Cart;
