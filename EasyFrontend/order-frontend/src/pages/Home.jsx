// src/pages/OrderPage.jsx
import React, { useEffect, useState } from 'react';
import { Link } from "react-router-dom";
import { FiShoppingCart } from "react-icons/fi";
import axios from 'axios';

function OrderPage() {
  const [products, setProducts] = useState({});
  const [cart, setCart] = useState([]);
  const [deskName, setDeskName] = useState('');
  const [businessName, setBusinessName] = useState('');
  const token = localStorage.getItem("token");
  const username = localStorage.getItem("username");
  const businessNameStorage = localStorage.getItem("business_name");

  useEffect(() => {
    setDeskName(username ? username.replace(/-/g, ' ').toUpperCase() : '');
    setBusinessName(businessNameStorage || '');
    initCartAndProducts();
    const cleanup = initWebSocket();
    return () => {
      if (typeof cleanup === 'function') cleanup();
    };
  }, []);

  const initCartAndProducts = async () => {
    await createCartIfNotExists();
    await fetchProducts();
  };

  const initWebSocket = () => {
    const deskSlug = localStorage.getItem("username");
    if (!deskSlug) return;

    const socket = new WebSocket(`ws://${process.env.REACT_APP_API_BASE_URL.replace("http://", "")}/ws/desk/${deskSlug}/`);

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "logout") {
        localStorage.removeItem("token");
        localStorage.removeItem("username");
        localStorage.removeItem("desk_id");
        localStorage.removeItem("business_name");
        window.location.href = "/logout";
      }
    };

    socket.onerror = (error) => console.error("WebSocket Hatası:", error);
    socket.onclose = () => console.log("WebSocket bağlantısı kapandı");

    return () => socket.close();
  };

  const createCartIfNotExists = async () => {
    try {
      await axios.post(`${process.env.REACT_APP_API_BASE_URL}/order/api/create-cart/`, {}, {
        headers: { Authorization: `Token ${token}` },
      });
      console.log("Cart oluşturuldu veya zaten vardı.");
    } catch (err) {
      if (err.response?.data?.message === "Cart already exists") {
        console.log("Zaten aktif sepet mevcut.");
      } else {
        console.error("Cart oluşturulurken hata:", err);
      }
    }
  };

  const fetchProducts = async () => {
    try {
      const res = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/order/api/produces/`, {
        headers: { Authorization: `Token ${token}` },
      });
      setProducts(res.data.produce_dict);
    } catch (error) {
      console.error("Ürünler alınamadı:", error);
    }
  };

  const addToCart = async (item) => {
    try {
      await axios.post(`${process.env.REACT_APP_API_BASE_URL}/order/api/add-to-cart/`, {
        produce_id: item.id,
        quantity: 1,
      }, {
        headers: { Authorization: `Token ${token}` },
      });

      setCart((prev) => {
        const existing = prev.find((p) => p.id === item.id);
        if (existing) {
          return prev.map((p) =>
            p.id === item.id ? { ...p, quantity: p.quantity + 1 } : p
          );
        } else {
          return [...prev, { ...item, quantity: 1 }];
        }
      });
    } catch (error) {
      console.error("Sepete ekleme hatası:", error);
      alert("Sepete eklenemedi.");
    }
  };

  return (
    <div className="p-4 font-amatic text-black">
      {/* Başlık */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-4xl text-center items-center font-bold tracking-wider">{`KOLAY MENÜ -  ${deskName}`}</h1>
        <Link
          to="/cart"
          className="flex gap-2 bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 px-6 rounded-full shadow-md"
        >
          <FiShoppingCart size={24} />
          Sepetim
        </Link>
      </div>

      {/* Ürünler */}
      {Object.keys(products).map((type) => (
        <div key={type} className="mb-10">
          <h2 className="text-3xl font-semibold mb-4">{type}</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
            {products[type].map((p) => (
              <div key={p.id} className="border rounded-2xl overflow-hidden shadow hover:shadow-lg transition">
                <img
                  src={`${process.env.REACT_APP_API_BASE_URL}${p.image}`}
                  alt={p.name}
                  loading="lazy"
                  className="h-40 w-full object-cover"
                />
                <div className="p-4">
                  <h3 className="text-2xl font-bold">{p.name}</h3>
                  <p className="text-lg mt-1 mb-3">{p.price} ₺</p>
                  <button
                    className="w-full bg-green-500 hover:bg-green-600 text-white font-bold py-2 rounded-full"
                    onClick={() => addToCart(p)}
                  >
                    Sepete Ekle
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}

      {/* Sepet */}
      {cart.length > 0 && (
        <div className="mt-12">
          <h2 className="text-2xl font-bold mb-4">Sepetiniz</h2>
          {cart.map((item) => (
            <div key={item.id} className="flex justify-between py-2 border-b">
              <span>{item.name} x {item.quantity}</span>
              <span>{(item.price * item.quantity).toFixed(2)} ₺</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default OrderPage;
