import { useState } from "react";
import { useApi } from "../../hooks/useApi";

export default function CreateFolderModal({ parentId, onSuccess }) {
  const [isOpen, setIsOpen] = useState(false);
  const [folderName, setFolderName] = useState("");
  const { request } = useApi();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await request({
        method: "POST",
        url: "/cloud/folders/create/",
        data: {
          name: folderName,
          parent_id: parentId,
        },
      });
      setIsOpen(false);
      setFolderName("");
      onSuccess(); // yeniden listele
    } catch (err) {
      console.error("Klasör oluşturma hatası:", err);
    }
  };

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        + Yeni Klasör
      </button>

      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
          <form
            onSubmit={handleSubmit}
            className="bg-white p-6 rounded shadow-lg w-80 space-y-4"
          >
            <h2 className="text-lg font-bold text-gray-800">Klasör Oluştur</h2>

            <input
              type="text"
              value={folderName}
              onChange={(e) => setFolderName(e.target.value)}
              placeholder="Klasör adı"
              className="w-full border px-3 py-2 rounded"
              required
            />

            <div className="flex justify-between">
              <button
                type="button"
                onClick={() => setIsOpen(false)}
                className="text-gray-500 hover:underline"
              >
                Vazgeç
              </button>
              <button
                type="submit"
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                Oluştur
              </button>
            </div>
          </form>
        </div>
      )}
    </>
  );
}
