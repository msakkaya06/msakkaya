// src/pages/OrderPage.jsx
import React, { useEffect, useState } from 'react';
import { Link } from "react-router-dom";
import { FiShoppingCart } from "react-icons/fi";
import axios from 'axios';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

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
    return () => {
      socket.onmessage = null;
      socket.onerror = null;
      socket.onclose = null;
      socket.close();
    };
    

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
        toast.error("Cart oluşturulamadı!");
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
      toast.error("Ürünler yüklenemedi!");
    }
  };

  const addToCart = async (item) => {
    try {
      await axios.post(
        `${process.env.REACT_APP_API_BASE_URL}/order/api/add-to-cart/`,
        {
          produce_id: item.id,
          quantity: 1,
        },
        {
          headers: {
            Authorization: `Token ${token}`,
          },
        }
      );

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

      toast.success(`${item.name} sepete eklendi! 🎉`);
    } catch (error) {
      console.error("Sepete ekleme hatası:", error);
      toast.error("Sepete eklenemedi ❌ Sayfayı Yenileyin veya QR Kod Yeniden Okutun ");
    }
  };

  return (
    <div className="p-4 relative font-montserrat">
      {/* Toast Container */}
      <ToastContainer position="top-center" autoClose={2000} hideProgressBar={false} />

      <div className="flex justify-between items-center mb-6">
        <h1 className="text-5xl font-bold">{businessName}</h1>
        <Link
          to="/cart"
          className="flex items-center gap-2 bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded"
        >
          <FiShoppingCart size={20} />
          Sepetim
        </Link>
      </div>

      <h2 className="text-3xl mb-6">Masa: {deskName}</h2>

      {Object.keys(products).map((type) => (
        <div key={type} className="mb-8">
          <h2 className="text-4xl font-semibold mb-4">{type}</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {products[type].map((p) => (
              <div key={p.id} className="border p-4 rounded-lg shadow hover:shadow-lg transition duration-300">
                <img
                  src={`${process.env.REACT_APP_API_BASE_URL}${p.image}`}
                  alt={p.name}
                  className="h-40 w-full object-cover mb-4 rounded-md"
                  loading="lazy"
                />
                <h3 className="text-2xl font-medium">{p.name}</h3>
                <p className="text-xl mb-2">{p.price} ₺</p>
                <button
                  className="mt-2 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded text-xl"
                  onClick={() => addToCart(p)}
                >
                  Sepete Ekle
                </button>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

export default OrderPage;
