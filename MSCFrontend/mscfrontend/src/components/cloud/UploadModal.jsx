import { useState } from "react";
import { useApi } from "../../hooks/useApi";

export default function UploadModal({ folderId, onSuccess }) {
  const [isOpen, setIsOpen] = useState(false);
  const [file, setFile] = useState(null);
  const { request } = useApi();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("folder_id", folderId ?? "");

    try {
      await request({
        method: "POST",
        url: "/cloud/files/upload/",
        data: formData,
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setIsOpen(false);
      setFile(null);
      onSuccess(); // dosyaları yenile
    } catch (err) {
      console.error("Yükleme hatası:", err);
    }
  };

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
      >
        📤 Dosya Yükle
      </button>

      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
          <form
            onSubmit={handleSubmit}
            className="bg-white p-6 rounded shadow-lg w-80 space-y-4"
          >
            <h2 className="text-lg font-bold text-gray-800">Dosya Yükle</h2>

            <input
              type="file"
              onChange={(e) => setFile(e.target.files[0])}
              className="w-full"
              required
            />

            <div className="flex justify-between">
              <button
                type="button"
                onClick={() => {
                  setIsOpen(false);
                  setFile(null);
                }}
                className="text-gray-500 hover:underline"
              >
                Vazgeç
              </button>
              <button
                type="submit"
                className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
              >
                Yükle
              </button>
            </div>
          </form>
        </div>
      )}
    </>
  );
}
