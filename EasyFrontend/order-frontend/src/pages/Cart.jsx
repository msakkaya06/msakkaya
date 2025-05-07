import axios from "axios";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast, ToastContainer } from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';

const Cart = () => {
  const [pendingItems, setPendingItems] = useState([]);
  const [confirmedItems, setConfirmedItems] = useState([]);
  const [cartId, setCartId] = useState(null);
  const [totalPrice, setTotalPrice] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    fetchCart();
    const businessId = localStorage.getItem("business_id");
    if (!businessId) return;
  
    const socket = new WebSocket(`ws://${process.env.REACT_APP_API_BASE_URL.replace("http://", "")}/ws/business/${businessId}/`);
  
    socket.onopen = () => console.log("Business WS bağlantısı kuruldu");
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log("Business WS mesajı:", data);
      // İstersen buraya toast koyabilirsin
    };
    socket.onerror = (err) => console.error("Business WS hatası:", err);
    socket.onclose = () => console.log("Business WS bağlantısı kapandı");
  
    return () => socket.close();
  }, []);

  const fetchCart = () => {
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
      .catch((err) => {
        console.error("Sepet verisi alınamadı:", err);
        toast.error("Sepet verisi alınamadı!");
      });
  };

  const handleConfirmOrder = () => {
    const token = localStorage.getItem("token");

    axios
      .post(`${process.env.REACT_APP_API_BASE_URL}/order/api/cart/${cartId}/to-order/`, {}, {
        headers: {
          Authorization: `Token ${token}`,
        },
      })
      .then((res) => {
        toast.success("Siparişiniz başarıyla oluşturuldu!");
        setTimeout(() => navigate("/"), 1000);
      })
      .catch((err) => {
        console.error("Sipariş onayı başarısız:", err);
        toast.error("Sipariş onaylanamadı!");
      });
  };

  const handleIncrease = (itemId) => {
    const token = localStorage.getItem("token");

    axios.post(`${process.env.REACT_APP_API_BASE_URL}/order/api/add-to-cart/`, {
      produce_id: itemId,
      quantity: 1,
    }, {
      headers: { Authorization: `Token ${token}` },
    }).then(() => {
      toast.success("Ürün adedi artırıldı!");
      fetchCart();
    }).catch((err) => {
      console.error("Arttırma hatası:", err);
      toast.error("Adet artırılamadı!");
    });
  };

  const handleDecrease = (cartItemId) => {
    const token = localStorage.getItem("token");

    axios.post(`${process.env.REACT_APP_API_BASE_URL}/order/api/decrease-cart-item/`, {
      cart_item_id: cartItemId,
    }, {
      headers: { Authorization: `Token ${token}` },
    }).then(() => {
      toast.success("Ürün adedi azaltıldı!");
      fetchCart();
    }).catch((err) => {
      console.error("Azaltma hatası:", err);
      toast.error("Adet azaltılamadı!");
    });
  };

  return (
    <div className="p-4 font-montserrat relative">
      <ToastContainer position="top-center" autoClose={2000} hideProgressBar={false} />

      <h1 className="text-4xl font-bold mb-6">Sepet</h1>

      <h2 className="text-2xl font-semibold mt-4 mb-2">🕐 Bekleyen Ürünler</h2>
      {pendingItems.length === 0 ? (
        <p className="text-gray-600">Onay bekleyen ürün yok.</p>
      ) : (
        pendingItems.map((item) => (
          <div key={item.id} className="border rounded p-4 mb-2 bg-yellow-100 shadow-md flex items-center justify-between">
            <div>
              <p className="text-xl font-semibold">{item.produce.name}</p>
              <p>Adet: {item.quantity}</p>
              <p>Birim Fiyat: {item.unit_price} ₺</p>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => handleDecrease(item.id)}
                className="bg-red-500 hover:bg-red-600 text-white rounded-full w-8 h-8 flex items-center justify-center"
              >
                -
              </button>
              <button
                onClick={() => handleIncrease(item.produce.id)}
                className="bg-green-500 hover:bg-green-600 text-white rounded-full w-8 h-8 flex items-center justify-center"
              >
                +
              </button>
            </div>
          </div>
        ))
      )}

      <h2 className="text-2xl font-semibold mt-6 mb-2">✅ Onaylanmış Ürünler</h2>
      {confirmedItems.length === 0 ? (
        <p className="text-gray-600">Onaylanmış ürün bulunmamaktadır.</p>
      ) : (
        confirmedItems.map((item) => (
          <div key={item.id} className="border rounded p-4 mb-2 bg-green-100 shadow-md">
            <p className="text-xl font-semibold">{item.produce.name}</p>
            <p>Adet: {item.quantity}</p>
            <p>Birim Fiyat: {item.unit_price} ₺</p>
          </div>
        ))
      )}

      <div className="mt-6 text-right font-semibold text-2xl">
        Toplam Tutar: {totalPrice} ₺
      </div>

      <div className="flex gap-4 mt-6">
        {pendingItems.length > 0 && (
          <button
            onClick={handleConfirmOrder}
            className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 rounded text-xl"
          >
            Siparişi Onayla
          </button>
        )}
        <button
          onClick={() => navigate("/")}
          className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-6 rounded text-xl"
        >
          Menüye Dön
        </button>
      </div>
    </div>
  );
};

export default Cart;
