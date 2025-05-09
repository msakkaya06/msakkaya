import { useEffect, useState } from "react";
import axios from "../api/axios";

export default function ProfilePage() {
  const [user, setUser] = useState(null);
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
  });
  const [message, setMessage] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("access");
    if (token) {
      axios
        .get("/auth/me/", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          setUser(res.data);
          setForm({
            first_name: res.data.first_name || "",
            last_name: res.data.last_name || "",
            email: res.data.email || "",
          });
        })
        .catch((err) => console.error("Profil alınamadı:", err));
    }
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const token = localStorage.getItem("access");
      const response = await axios.patch("/auth/me/", form, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setMessage("Profil başarıyla güncellendi.");
      setUser(response.data);
    } catch (err) {
      setMessage("Güncelleme başarısız oldu.");
      console.error("Güncelleme hatası:", err);
    }
  };

  if (!user) return <div className="p-8">Yükleniyor...</div>;

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100 p-6">
      <div className="bg-white rounded-xl shadow-md w-full max-w-lg p-6 space-y-6">
        <div className="flex items-center gap-4">
          <img
            src={`https://ui-avatars.com/api/?name=${user.first_name}+${user.last_name}&background=0D8ABC&color=fff`}
            alt="Avatar"
            className="w-20 h-20 rounded-full shadow"
          />
          <div>
            <h2 className="text-2xl font-bold text-gray-800">
              {user.first_name} {user.last_name}
            </h2>
            <p className="text-sm text-gray-500">{user.email}</p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Ad</label>
            <input
              type="text"
              name="first_name"
              value={form.first_name}
              onChange={handleChange}
              className="w-full border rounded-md px-4 py-2 mt-1"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Soyad</label>
            <input
              type="text"
              name="last_name"
              value={form.last_name}
              onChange={handleChange}
              className="w-full border rounded-md px-4 py-2 mt-1"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              className="w-full border rounded-md px-4 py-2 mt-1"
            />
          </div>

          {message && <p className="text-sm text-green-600">{message}</p>}

          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition"
          >
            Güncelle
          </button>
        </form>
      </div>
    </div>
  );
}
