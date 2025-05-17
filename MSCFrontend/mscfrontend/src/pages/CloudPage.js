import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useApi } from "../hooks/useApi";
import FolderCard from "../components/cloud/FolderCard";
import FileCard from "../components/cloud/FileCard";
import CreateFolderModal from "../components/cloud/CreateFolderModal";
import UploadModal from "../components/cloud/UploadModal";

export default function CloudPage() {
    const { folderId } = useParams(); // URL'den klasör id
    const navigate = useNavigate();
    const currentFolderId = folderId === "null" ? null : folderId;
    const [currentFolderName, setCurrentFolderName] = useState("Ana Klasör");

    const [folders, setFolders] = useState([]);
    const [files, setFiles] = useState([]);
    const [viewMode, setViewMode] = useState("grid"); // "grid" | "list"

    const { request } = useApi();
const fetchData = async () => {
  const folderPromise = request({
    url: `/cloud/folders/?parent_id=${currentFolderId ?? "null"}`,
  });
  const filePromise = request({
    url: `/cloud/files/?folder_id=${currentFolderId ?? "null"}`,
  });

  if (currentFolderId) {
    const folderDetail = await request({ url: `/cloud/folders/${currentFolderId}/` });
    setCurrentFolderName(folderDetail.name);
  } else {
    setCurrentFolderName("Ana Klasör");
  }

  const [folderRes, fileRes] = await Promise.all([folderPromise, filePromise]);
  setFolders(folderRes);
  setFiles(fileRes);
};


    useEffect(() => {
        fetchData();
    }, [currentFolderId]);

    return (

        <div className="p-6 space-y-6">
            <div className="flex justify-between items-center">
                <div className="text-sm text-gray-600 space-x-2">
                    {currentFolderId ? (
                        <>
                            <button
                                className="underline hover:text-blue-600"
                                onClick={() => navigate("/cloud")}
                            >
                                Ana Klasör
                            </button>
                            <span>/</span>
                            <span className="font-medium text-gray-800">{currentFolderName}</span>
                        </>
                    ) : (
                        <span className="font-medium text-gray-800">Ana Klasör</span>
                    )}
                </div>

                <h1 className="text-2xl font-bold text-gray-800">Dosya Yöneticisi</h1>

                <div className="flex items-center gap-3">
                    <button
                        onClick={() => setViewMode("grid")}
                        className={`text-sm ${viewMode === "grid" ? "font-bold" : "text-gray-500"}`}
                    >
                        🟦 Döşeme
                    </button>
                    <button
                        onClick={() => setViewMode("list")}
                        className={`text-sm ${viewMode === "list" ? "font-bold" : "text-gray-500"}`}
                    >
                        📄 Liste
                    </button>
                </div>
            </div>

            <div className="flex space-x-4">
                <CreateFolderModal parentId={currentFolderId} onSuccess={fetchData} />
                <UploadModal folderId={currentFolderId} onSuccess={fetchData} />
                {folderId && (
                    <button
                        onClick={() => navigate("/cloud")}
                        className="text-sm text-gray-500 underline"
                    >
                        ⬅ Geri Dön
                    </button>
                )}
            </div>

            {viewMode === "grid" ? (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
                    {folders.map((folder) => (
                        <FolderCard
                            key={folder.id}
                            folder={folder}
                            onClick={() => navigate(`/cloud/${folder.id}`)}
                        />
                    ))}
                    {files.map((file) => (
                        <FileCard key={file.id} file={file} />
                    ))}
                </div>
            ) : (
                <div className="mt-6 space-y-2">
                    <div className="grid grid-cols-2 md:grid-cols-3 font-semibold text-gray-700 text-sm border-b pb-1">
                        <span>Ad</span>
                        <span>Boyut</span>
                        <span className="hidden md:inline">Yüklenme</span>
                    </div>

                    {folders.map((folder) => (
                        <div
                            key={folder.id}
                            onClick={() => navigate(`/cloud/${folder.id}`)}
                            className="grid grid-cols-2 md:grid-cols-3 hover:bg-gray-100 cursor-pointer text-sm py-1 border-b"
                        >
                            <span>📁 {folder.name}</span>
                            <span>—</span>
                            <span className="hidden md:inline">
                                {new Date(folder.created_at).toLocaleString("tr-TR")}
                            </span>
                        </div>
                    ))}

                    {files.map((file) => (
                        <div
                            key={file.id}
                            className="grid grid-cols-2 md:grid-cols-3 hover:bg-gray-100 text-sm py-1 border-b"
                        >
                            <span>📄 {file.name}</span>
                            <span>—</span>
                            <span className="hidden md:inline">
                                {new Date(file.uploaded_at).toLocaleString("tr-TR")}
                            </span>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
