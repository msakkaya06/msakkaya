// src/pages/OrderPage.jsx
import React, { useEffect, useState } from 'react';
import { Link } from "react-router-dom";
import { FiShoppingCart } from "react-icons/fi"; // Sepet simgesi
import axios from 'axios';

function OrderPage() {
  const [products, setProducts] = useState({});
  const [cart, setCart] = useState([]);
  const [token] = useState(localStorage.getItem('token'));

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const res = await axios.get("http://192.168.137.1:8080/order/api/produces/", {
        headers: {
          Authorization: `Token ${token}`
        }
      });
      setProducts(res.data.produce_dict);
    } catch (error) {
      console.error("Ürünler alınamadı:", error);
    }
  };

  const addToCart = (item) => {
    setCart((prev) => {
      const existing = prev.find(p => p.id === item.id);
      if (existing) {
        return prev.map(p => p.id === item.id ? { ...p, quantity: p.quantity + 1 } : p);
      } else {
        return [...prev, { ...item, quantity: 1 }];
      }
    });
  };


  // return bloğunun üstüne bir yerde olsun

  
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Ürünler</h1>
      <Link
        to="/cart"
        className="flex items-center gap-2 bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded"
      >
        <FiShoppingCart size={20} />
        Sepetim
      </Link>
      {Object.keys(products).map((type) => (
        <div key={type} className="mb-6">
          <h2 className="text-xl font-semibold mb-2">{type}</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {products[type].map((p) => (
              <div key={p.id} className="border p-3 rounded-lg shadow">
                <img src={`http://192.168.137.1:8080${p.image}`} alt={p.name} className="h-32 w-full object-cover mb-2" />
                <h3 className="font-medium">{p.name}</h3>
                <p>{p.price} ₺</p>
                <button
                  className="mt-2 bg-green-600 text-white px-3 py-1 rounded"
                  onClick={() => addToCart(p)}
                >
                  Sepete Ekle
                </button>
              </div>
            ))}
          </div>
        </div>
      ))}
      

      <div className="mt-8">
        <h2 className="text-xl font-bold mb-2">Sepet</h2>
        {cart.map((item) => (
          <div key={item.id} className="flex justify-between py-2 border-b">
            <span>{item.name} x {item.quantity}</span>
            <span>{(item.price * item.quantity).toFixed(2)} ₺</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default OrderPage;
