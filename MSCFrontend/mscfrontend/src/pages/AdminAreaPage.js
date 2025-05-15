import { useEffect, useState } from "react";
import { useModal } from "../context/ModalContext";
import { useApi } from "../hooks/useApi";
import { useDebounce } from "../hooks/useDebounce";

export default function AdminAreaPage() {
  const [users, setUsers] = useState([]);
  const [pagination, setPagination] = useState({ next: null, previous: null, count: 0 });
  const [page, setPage] = useState(1);
  const [filterStatus, setFilterStatus] = useState("all");
  const [filterAdmin, setFilterAdmin] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");
  const debouncedSearch = useDebounce(searchQuery);
  const { openModal } = useModal();
  const { request, loading } = useApi();
  const pageSize = 10;
  const totalPages = Math.ceil(pagination.count / pageSize);

  const fetchUsers = async ({
    showLoading = false,
    page = 1,
    status = filterStatus,
    admin = filterAdmin,
    search = searchQuery,
  } = {}) => {
    let url = `/auth/admin/users/?page=${page}`;
    if (status === "active") url += "&is_active=true";
    else if (status === "inactive") url += "&is_active=false";
    if (admin === "admin") url += "&is_admin=true";
    else if (admin === "normal") url += "&is_admin=false";
    if (search) url += `&search=${encodeURIComponent(search)}`;

    try {
      const data = await request({ url, silent: !showLoading });
      setUsers(data.results);
      setPagination({
        next: data.next,
        previous: data.previous,
        count: data.count,
      });
      setPage(page);
    } catch {}
  };

useEffect(() => {
  fetchUsers({ showLoading: true, page, search: debouncedSearch });
}, [debouncedSearch, filterStatus, filterAdmin, page]);

  const makeAdmin = async (userId) => {
    await request({ method: "POST", url: "/auth/make-admin/", data: { user_id: userId }, silent: true });
    fetchUsers({ page });
  };

  const removeAdmin = async (userId) => {
    await request({ method: "POST", url: "/auth/remove-admin/", data: { user_id: userId }, silent: true });
    fetchUsers({ page });
  };

  const toggleActive = async (userId) => {
    await request({ method: "POST", url: "/auth/toggle-active/", data: { user_id: userId }, silent: true });
    fetchUsers({ page });
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6 text-gray-800">Admin Panel – Kullanıcı Listesi</h1>

      {/* Filtre & Arama */}
      <div className="mb-6 flex flex-wrap gap-6 items-center text-sm">
        {/* Durum filtresi */}
        <div className="flex gap-2 items-center">
          <label className="text-gray-600">Durum:</label>
          <select
            value={filterStatus}
            onChange={(e) => {
              setFilterStatus(e.target.value);
              setPage(1);
            }}
            className="border px-3 py-1 rounded"
          >
            <option value="all">Tümü</option>
            <option value="active">Sadece Aktif</option>
            <option value="inactive">Sadece Pasif</option>
          </select>
        </div>

        {/* Rol filtresi */}
        <div className="flex gap-2 items-center">
          <label className="text-gray-600">Rol:</label>
          <select
            value={filterAdmin}
            onChange={(e) => {
              setFilterAdmin(e.target.value);
              setPage(1);
            }}
            className="border px-3 py-1 rounded"
          >
            <option value="all">Tümü</option>
            <option value="admin">Sadece Admin</option>
            <option value="normal">Normal Kullanıcılar</option>
          </select>
        </div>

        {/* Arama kutusu */}
        <div className="flex gap-2 items-center">
          <label className="text-gray-600">Ara:</label>
          <input
            type="text"
            placeholder="İsim, kullanıcı adı veya email"
            value={searchQuery}
            onChange={(e) => {
              setSearchQuery(e.target.value);
              setPage(1);
            }}
            className="border px-3 py-1 rounded w-64"
          />
        </div>
      </div>

      {/* Skeleton */}
      {loading ? (
        <div className="animate-pulse">
          {[...Array(10)].map((_, idx) => (
            <div key={idx} className="grid grid-cols-7 items-center gap-4 bg-white px-4 py-3 border-b">
              <div className="w-10 h-10 bg-gray-300 rounded-full" />
              <div className="h-4 bg-gray-300 rounded w-full col-span-1" />
              <div className="h-4 bg-gray-300 rounded w-full col-span-1" />
              <div className="h-4 bg-gray-300 rounded w-full col-span-1" />
              <div className="h-4 bg-gray-300 rounded w-3/4 col-span-1" />
              <div className="h-4 bg-gray-300 rounded w-2/3 col-span-1" />
              <div className="flex space-x-2">
                <div className="h-6 w-16 bg-gray-300 rounded" />
                <div className="h-6 w-16 bg-gray-300 rounded" />
              </div>
            </div>
          ))}
        </div>
      ) : (
        <>
          {/* Tablo */}
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
                    <td className="px-4 py-2 space-x-2" onClick={(e) => e.stopPropagation()}>
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
                        onClick={() => toggleActive(user.id)}
                        className={`text-xs ${user.is_active ? "bg-red-600" : "bg-green-600"} text-white px-3 py-1 rounded hover:opacity-90`}
                      >
                        {user.is_active ? "Pasifleştir" : "Aktifleştir"}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Sayfalama */}
          <div className="flex justify-between items-center mt-6 text-sm">
            <div className="space-x-2">
              <button onClick={() => setPage(1)} disabled={page === 1} className="px-3 py-1 rounded bg-gray-200 disabled:opacity-50">⏮ İlk</button>
              <button onClick={() => setPage((p) => Math.max(p - 1, 1))} disabled={!pagination.previous} className="px-3 py-1 rounded bg-gray-200 disabled:opacity-50">← Önceki</button>
              <button onClick={() => setPage((p) => p + 1)} disabled={!pagination.next} className="px-3 py-1 rounded bg-gray-200 disabled:opacity-50">Sonraki →</button>
              <button onClick={() => setPage(totalPages)} disabled={page === totalPages} className="px-3 py-1 rounded bg-gray-200 disabled:opacity-50">⏭ Son</button>
            </div>
            <div className="text-gray-600">Sayfa {page} / {totalPages} — Toplam {pagination.count} kullanıcı</div>
          </div>
        </>
      )}
    </div>
  );
}
