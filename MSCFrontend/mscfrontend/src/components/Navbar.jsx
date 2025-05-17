import { Link, useNavigate, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "../api/axios";

export default function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("access");
    if (token) {
      axios
        .get("/auth/me/", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => setUser(res.data))
        .catch((err) => {
          console.error("Kullanıcı bilgisi alınamadı:", err);
          localStorage.removeItem("access");
          localStorage.removeItem("refresh");
          navigate("/login");
        });
    }
  }, []);

  if (location.pathname === "/login" || location.pathname === "/register") {
    return null;
  }

  return (
    <nav className="bg-white shadow p-4 flex justify-between items-center">
      <Link to="/cloud" className="text-xl font-bold text-blue-600">MSC Cloud</Link>

      {user && (
        <div className="flex items-center gap-4">
          <span className="text-gray-700">{user.first_name} {user.last_name}</span>
          <Link to="/me" className="text-sm text-blue-500 hover:underline">Profil</Link>

{Array.isArray(user.groups) && user.groups.includes("admin") && (
  <Link to="/admin-area" className="text-sm text-blue-500 hover:underline">
    Yönetim Paneli
  </Link>
)}


          <button
            onClick={() => {
              localStorage.removeItem("access");
              localStorage.removeItem("refresh");
              navigate("/login");
            }}
            className="text-sm text-red-500 hover:underline"
          >
            Çıkış Yap
          </button>
        </div>
      )}
    </nav>
  );
}
