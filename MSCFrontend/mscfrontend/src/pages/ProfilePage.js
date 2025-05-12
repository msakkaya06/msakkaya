import { useEffect, useRef, useState } from "react";
import axios from "../api/axios";

export default function ProfilePage() {
  const [user, setUser] = useState(null);
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
    profile_image: null,
  });
  const [message, setMessage] = useState("");
  const [showModal, setShowModal] = useState(false);

  const fileInputRef = useRef();

  // Şifre değiştirme formu
  const [passwordForm, setPasswordForm] = useState({
    old_password: "",
    new_password: "",
    new_password2: "",
  });
  const [passwordMessage, setPasswordMessage] = useState("");
  const [passwordError, setPasswordError] = useState("");

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
            profile_image: null,
          });
        })
        .catch((err) => console.error("Profil alınamadı:", err));
    }
  }, []);

  const handleChange = (e) => {
    if (e.target.name === "profile_image") {
      const file = e.target.files[0];
      setForm((prev) => ({ ...prev, profile_image: file }));
      handleImageUpload(file);
    } else {
      setForm({ ...form, [e.target.name]: e.target.value });
    }
  };

  const handleImageUpload = async (file) => {
    try {
      const token = localStorage.getItem("access");
      const formData = new FormData();
      formData.append("profile_image", file);

      const response = await axios.patch("/auth/me/", formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      });

      setUser((prev) => ({ ...prev, ...response.data }));
      setMessage("Profil fotoğrafı güncellendi.");
    } catch (err) {
      setMessage("Fotoğraf yükleme hatası.");
      console.error("Upload error:", err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const token = localStorage.getItem("access");
      const formData = new FormData();

      for (const key in form) {
        if (form[key] !== null && key !== "profile_image") {
          formData.append(key, form[key]);
        }
      }

      const response = await axios.patch("/auth/me/", formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      });

      setMessage("Profil başarıyla güncellendi.");
      setUser({ ...user, ...response.data });
    } catch (err) {
      setMessage("Güncelleme başarısız oldu.");
      console.error("Güncelleme hatası:", err);
    }
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    setPasswordMessage("");
    setPasswordError("");

    try {
      const token = localStorage.getItem("access");

      const res = await axios.post("/auth/change-password/", passwordForm, {
        headers: { Authorization: `Bearer ${token}` },
      });

      setPasswordMessage(res.data.message);
      setPasswordForm({
        old_password: "",
        new_password: "",
        new_password2: "",
      });
    } catch (err) {
      setPasswordError(
        err.response?.data?.error || "Bir hata oluştu, tekrar deneyin."
      );
    }
  };

  if (!user) return <div className="p-8">Yükleniyor...</div>;

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100 p-6">
      <div className="bg-white rounded-xl shadow-md w-full max-w-lg p-6 space-y-6">
        <div className="flex flex-col items-center gap-2">
          <div
            className="relative cursor-pointer"
            onClick={() => fileInputRef.current.click()}
          >
            <img
              src={
                user.profile_image
                  ? `http://localhost:9090${user.profile_image}`
                  : `https://ui-avatars.com/api/?name=${user.first_name}+${user.last_name}&background=0D8ABC&color=fff`
              }
              alt="Avatar"
              className="w-24 h-24 rounded-full shadow border-2 border-blue-500 object-cover"
            />
            <p className="text-sm text-blue-500 mt-1 text-center">Değiştir</p>
            <input
              type="file"
              accept="image/*"
              name="profile_image"
              ref={fileInputRef}
              onChange={handleChange}
              className="hidden"
            />
          </div>

          <h2 className="text-xl font-bold text-gray-800">
            {user.first_name} {user.last_name}
          </h2>
          <p className="text-sm text-gray-500">{user.email}</p>
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

          <div className="flex justify-between items-center">
            <button
              type="submit"
              className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition"
            >
              Güncelle
            </button>
            <button
              type="button"
              onClick={() => setShowModal(true)}
              className="text-sm text-blue-600 hover:underline"
            >
              Şifreyi Değiştir
            </button>
          </div>
        </form>
      </div>

      {/* 🔐 Şifre Değiştirme Modali */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md shadow-xl">
            <h2 className="text-xl font-bold mb-4 text-gray-800">Şifre Değiştir</h2>

            <form onSubmit={handlePasswordChange} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Eski Şifre</label>
                <input
                  type="password"
                  name="old_password"
                  value={passwordForm.old_password}
                  onChange={(e) =>
                    setPasswordForm({ ...passwordForm, old_password: e.target.value })
                  }
                  className="w-full border rounded-md px-4 py-2 mt-1"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Yeni Şifre</label>
                <input
                  type="password"
                  name="new_password"
                  value={passwordForm.new_password}
                  onChange={(e) =>
                    setPasswordForm({ ...passwordForm, new_password: e.target.value })
                  }
                  className="w-full border rounded-md px-4 py-2 mt-1"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Yeni Şifre (Tekrar)</label>
                <input
                  type="password"
                  name="new_password2"
                  value={passwordForm.new_password2}
                  onChange={(e) =>
                    setPasswordForm({ ...passwordForm, new_password2: e.target.value })
                  }
                  className="w-full border rounded-md px-4 py-2 mt-1"
                  required
                />
              </div>

              {passwordError && <p className="text-sm text-red-500">{passwordError}</p>}
              {passwordMessage && <p className="text-sm text-green-600">{passwordMessage}</p>}

              <div className="flex justify-between mt-4">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="text-sm text-gray-500 hover:underline"
                >
                  Vazgeç
                </button>
                <button
                  type="submit"
                  className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition"
                >
                  Güncelle
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
