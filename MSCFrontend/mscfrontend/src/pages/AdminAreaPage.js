import { useEffect, useState } from "react";
import axios from "../api/axios";
import { useToast } from "../context/ToastContext";
import { useModal } from "../context/ModalContext";


export default function AdminAreaPage() {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");
  const { notify } = useToast();
  const { openModal } = useModal();


  const fetchUsers = async () => {
    try {
      const token = localStorage.getItem("access");
      const res = await axios.get("/auth/admin/users/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUsers(res.data);
    } catch (err) {
      setError("Kullanıcı listesi alınamadı.");
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const makeAdmin = async (userId) => {
    try {
      const token = localStorage.getItem("access");
      await axios.post("/auth/make-admin/", { user_id: userId }, {
        headers: { Authorization: `Bearer ${token}` },
      });
      notify("Kullanıcı admin yapıldı", "success");
      fetchUsers();
    } catch {
      notify("Admin yapma başarısız", "error");
    }
  };

  const removeAdmin = async (userId) => {
    try {
      const token = localStorage.getItem("access");
      await axios.post("/auth/remove-admin/", { user_id: userId }, {
        headers: { Authorization: `Bearer ${token}` },
      });
      notify("Admin yetkisi kaldırıldı", "success");
      fetchUsers();
    } catch {
      notify("İşlem başarısız", "error");
    }
  };

  const toggleActive = async (userId, currentStatus) => {
    try {
      const token = localStorage.getItem("access");
      await axios.post("/auth/toggle-active/", { user_id: userId }, {
        headers: { Authorization: `Bearer ${token}` },
      });
      notify(currentStatus ? "Kullanıcı pasifleştirildi" : "Kullanıcı aktifleştirildi", "info");
      fetchUsers();
    } catch {
      notify("Aktiflik değiştirilemedi", "error");
    }
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6 text-gray-800">Admin Panel – Kullanıcı Listesi</h1>

      {error && <p className="text-red-500 mb-4">{error}</p>}

      <div className="overflow-x-auto">
        <table className="w-full border text-sm text-left">
          <thead className="bg-gray-200 text-gray-600 uppercase text-xs">
            <tr>
              <th className="px-4 py-3">Avatar</th>

              <th className="px-4 py-3">Ad Soyad</th>
              <th className="px-4 py-3">Email</th>
                  <th className="px-4 py-3">Kullanıcı Adı</th>
              <th className="px-4 py-3">Roller</th>
              <th className="px-4 py-3">Durum</th>
              <th className="px-4 py-3">İşlemler</th>
            </tr>
          </thead>
         <tbody>
  {users.map((user) => (
    <tr
      key={user.id}
      className="border-b hover:bg-gray-50 cursor-pointer"
      onClick={() =>
        openModal(
          <div>
            <h2 className="text-xl font-bold mb-4">Kullanıcı Detayları</h2>
            <div className="text-sm text-gray-700 space-y-2">
              <p><strong>Ad Soyad:</strong> {user.full_name}</p>
              <p><strong>Email:</strong> {user.email}</p>
              <p><strong>Kullanıcı Adı:</strong> {user.username}</p>

              <p><strong>Roller:</strong> {user.groups.join(", ") || "—"}</p>
              <p><strong>Durum:</strong> {user.is_active ? "Aktif" : "Pasif"}</p>
              <p><strong>Oluşturulma:</strong> {new Date(user.created_at).toLocaleString("tr-TR")}</p>
              {user.last_login && (
                <p><strong>Son Giriş:</strong> {new Date(user.last_login).toLocaleString("tr-TR")}</p>
              )}
            </div>
          </div>
        )
      }
    >
      <td className="px-4 py-2">
  <img
    src={
      user.profile_image
        ? `http://localhost:9090${user.profile_image}`
        : `https://ui-avatars.com/api/?name=${user.first_name}+${user.last_name}&background=0D8ABC&color=fff`
    }
    alt="avatar"
    className="w-10 h-10 rounded-full object-cover"
  />
</td>

      <td className="px-4 py-2">{user.full_name}</td>
      <td className="px-4 py-2">{user.email}</td>
      <td className="px-4 py-2">{user.username}</td>

      <td className="px-4 py-2">{user.groups.length ? user.groups.join(", ") : "—"}</td>
      <td className="px-4 py-2">
        {user.is_active ? (
          <span className="text-green-600 font-medium">Aktif</span>
        ) : (
          <span className="text-red-600 font-medium">Pasif</span>
        )}
      </td>
      <td
        className="px-4 py-2 space-x-2"
        onClick={(e) => e.stopPropagation()} // ❗ Modal yerine butona tıklamayı engellemez
      >
        {!user.groups.includes("admin") ? (
          <button
            onClick={() => makeAdmin(user.id)}
            className="text-xs bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
          >
            Admin Yap
          </button>
        ) : (
          <button
            onClick={() => removeAdmin(user.id)}
            className="text-xs bg-yellow-600 text-white px-3 py-1 rounded hover:bg-yellow-700"
          >
            Adminliği Kaldır
          </button>
        )}

        <button
          onClick={() => toggleActive(user.id, user.is_active)}
          className={`text-xs ${
            user.is_active ? "bg-red-600" : "bg-green-600"
          } text-white px-3 py-1 rounded hover:opacity-90`}
        >
          {user.is_active ? "Pasifleştir" : "Aktifleştir"}
        </button>
      </td>
    </tr>
  ))}
</tbody>

        </table>
      </div>
    </div>
  );
}
