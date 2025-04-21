// src/pages/OrderPage.jsx
import React, { useEffect, useState } from 'react';
import { Link } from "react-router-dom";
import { FiShoppingCart } from "react-icons/fi";
import axios from 'axios';

function OrderPage() {
    const [products, setProducts] = useState({});
    const [cart, setCart] = useState([]);
    const [deskName, setDeskName] = useState('');
    const token = localStorage.getItem("token");
    const username = localStorage.getItem("username"); // kullanıcı adı (desk.slug)

    useEffect(() => {
        setDeskName(username.replace(/-/g, ' ').toUpperCase()); // Başlıkta gösterilecek hali
        initCartAndProducts();
        const cleanup = initWebSocket();  // socket cleanup fonksiyonu döner

        return () => {
            if (typeof cleanup === 'function') cleanup();  // sayfa unload olunca socket kapatılır
        };
    }, []);

    const initCartAndProducts = async () => {
        await createCartIfNotExists();
        await fetchProducts();
    };
    const initWebSocket = async () => {
        const deskSlug = localStorage.getItem("username");
        if (!deskSlug) return;
        console.log(deskSlug);
        const socket = new WebSocket(`ws://${process.env.REACT_APP_API_BASE_URL.replace("http://", "")}/ws/desk/${deskSlug}/`);

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);

            if (data.type === "logout") {
                localStorage.removeItem("token");
                localStorage.removeItem("username");
                localStorage.removeItem("desk_id");
                localStorage.removeItem("business_name");

                window.location.href = "/logout"; // logout sayfasına yönlendir
            }
        };

        socket.onerror = (error) => console.error("WebSocket Hatası:", error);
        socket.onclose = () => console.log("WebSocket bağlantısı kapandı");

        return () => socket.close(); // Sayfa kapanınca bağlantıyı kapat

    }
    const createCartIfNotExists = async () => {
        try {
            await axios.post(`${process.env.REACT_APP_API_BASE_URL}/order/api/create-cart/`, {}, {
                headers: {
                    Authorization: `Token ${token}`,
                },
            });
            console.log("Cart oluşturuldu veya zaten vardı.");
        } catch (err) {
            if (err.response?.data?.message === "Cart already exists") {
                console.log("Zaten bir aktif sepet mevcut.");
            } else {
                console.error("Cart oluşturulurken hata:", err);
            }
        }
    };

    const fetchProducts = async () => {
        try {
            const res = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/order/api/produces/`, {
                headers: {
                    Authorization: `Token ${token}`
                }
            });
            setProducts(res.data.produce_dict);
        } catch (error) {
            console.error("Ürünler alınamadı:", error);
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
        } catch (error) {
            console.error("Sepete ekleme hatası:", error);
            alert("Sepete eklenemedi.");
        }
    };

    const releaseDesk = async () => {
        try {
            await axios.post(
                `${process.env.REACT_APP_API_BASE_URL}/order/api/release-desk/`,
                {},
                {
                    headers: {
                        Authorization: `Token ${token}`,
                    },
                }
            );
            //alert("Masa başarıyla boşa çekildi.");
            localStorage.removeItem("token");
            localStorage.removeItem("username");
            window.location.href = "/logout"; // Yönlendirme logout sayfasına

        } catch (error) {
            console.error("Masa boşa çekilemedi:", error);
            alert("Bir hata oluştu.");
        }
    };

    return (
        <div className="p-4">
            {/* Başlık */}
            <div className="flex justify-between items-center mb-4">
                <h1 className="text-2xl font-bold">
                    KOLAY MENÜ - {deskName}
                </h1>
                <div className="flex gap-2">
                    <Link
                        to="/cart"
                        className="flex items-center gap-2 bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded"
                    >
                        <FiShoppingCart size={20} />
                        Sepetim
                    </Link>
                    <button
                        onClick={releaseDesk}
                        className="bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded"
                    >
                        Masayı Boşa Çek
                    </button>
                </div>
            </div>

            {/* Ürünler */}
            {Object.keys(products).map((type) => (
                <div key={type} className="mb-6">
                    <h2 className="text-xl font-semibold mb-2">{type}</h2>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        {products[type].map((p) => (
                            <div key={p.id} className="border p-3 rounded-lg shadow">
                                <img
                                    src={`${process.env.REACT_APP_API_BASE_URL}${p.image}`}
                                    loading="lazy"
                                    alt={p.name}
                                    className="h-32 w-full object-cover mb-2 rounded"
                                />
                                <h3 className="font-medium">{p.name}</h3>
                                <p>{p.price} ₺</p>
                                <button
                                    className="mt-2 bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded"
                                    onClick={() => addToCart(p)}
                                >
                                    Sepete Ekle
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            ))}

            {/* Sepet Bilgisi */}
            {cart.length > 0 && (
                <div className="mt-8">
                    <h2 className="text-xl font-bold mb-2">Sepet</h2>
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
