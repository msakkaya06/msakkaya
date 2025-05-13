import { useState } from "react";
import axios from "../api/axios";
import { useToast } from "../context/ToastContext";
import { extractMessage } from "../utils/apiErrors";



export default function RegisterPage() {
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    first_name: "",
    last_name: "",
  });
  const { notify } = useToast();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };
const handleSubmit = async (e) => {
  e.preventDefault();
try {
  const loginRes = await axios.post("/auth/register/", form);
  const { access, refresh } = loginRes.data;

  localStorage.setItem("access", access);
  localStorage.setItem("refresh", refresh);

  const meRes = await axios.get("/auth/me/", {
    headers: { Authorization: `Bearer ${access}` },
  });

  notify(`Hoş geldin, ${meRes.data.full_name || meRes.data.username}!`, "success");

  setTimeout(() => {
    window.location.href = "/dashboard";
  }, 1500);

} catch (err) {
  console.error(err);
  notify(extractMessage(err), "error");
}

};


  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md space-y-4"
      >
        <h2 className="text-2xl font-bold text-center text-gray-800">Kayıt Ol</h2>

        <input
          type="text"
          name="first_name"
          placeholder="Ad"
          value={form.first_name}
          onChange={handleChange}
          className="w-full px-4 py-2 border rounded-md"
          required
        />
        <input
          type="text"
          name="last_name"
          placeholder="Soyad"
          value={form.last_name}
          onChange={handleChange}
          className="w-full px-4 py-2 border rounded-md"
          required
        />
        <input
          type="text"
          name="username"
          placeholder="Kullanıcı Adı"
          value={form.username}
          onChange={handleChange}
          className="w-full px-4 py-2 border rounded-md"
          required
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          className="w-full px-4 py-2 border rounded-md"
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Şifre"
          value={form.password}
          onChange={handleChange}
          className="w-full px-4 py-2 border rounded-md"
          required
        />

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition"
        >
          Kayıt Ol
        </button>
      </form>
    </div>
  );
}
