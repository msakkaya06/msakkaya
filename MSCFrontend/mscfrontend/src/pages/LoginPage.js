import { useState } from "react";
import axios from "../api/axios";
import { useToast } from "../context/ToastContext";


export default function LoginPage() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState(null);
  const { notify } = useToast();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await axios.post("/auth/login/", form);
      const { access, refresh } = response.data;

      localStorage.setItem("access", access);
      localStorage.setItem("refresh", refresh);

      const me = await axios.get("/auth/me/", {
        headers: { Authorization: `Bearer ${access}` },
      });

      notify(`Hoş geldin, ${me.data.full_name || me.data.username}!`, "success");

      setTimeout(() => {
        window.location.href = "/dashboard";
      }, 1500); // 1.5 saniye sonra yönlendir
    } catch (err) {
      console.error("Login hatası:", err);
      setError("Giriş başarısız");
    }
  };

  // return içeriği aşağıda devam eder...

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 relative overflow-hidden">
      {/* Arka plan yazısı */}
      {/* Arka plan yazıları */}
      <h1 className="absolute top-10 left-1/2 transform -translate-x-1/2 text-7xl md:text-9xl font-extrabold text-gray-300 tracking-wide select-none pointer-events-none z-0">
        MSC
      </h1>
      <h1 className="absolute top-28 left-1/2 transform -translate-x-1/2 text-7xl md:text-9xl font-extrabold text-blue-400 tracking-tight select-none pointer-events-none z-0 -mt-4">
        Cloud
      </h1>


      {/* Form kutusu */}
      <form
        onSubmit={handleSubmit}
        className="relative z-10 bg-white p-8 rounded-lg shadow-xl w-full max-w-sm"
      >
        <h2 className="text-2xl font-bold mb-6 text-center text-gray-700">Giriş Yap</h2>

        <div className="mb-4">
          <label className="block text-gray-600 mb-2">Kullanıcı Adı</label>
          <input
            type="text"
            name="username"
            value={form.username}
            onChange={handleChange}
            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div className="mb-6">
          <label className="block text-gray-600 mb-2">Şifre</label>
          <input
            type="password"
            name="password"
            value={form.password}
            onChange={handleChange}
            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        {error && (
          <p className="text-red-500 text-sm text-center mb-4">{error}</p>
        )}

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition"
        >
          Giriş Yap
        </button>
      </form>

    </div>
  );
}
