export default function FolderCard({ folder, onClick }) {
  return (
    <div
      onClick={onClick}
      className="cursor-pointer border rounded-lg shadow hover:shadow-md p-4 bg-white transition"
    >
      <div className="flex items-center space-x-3">
        <svg
          className="w-6 h-6 text-yellow-500"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path d="M2 4a2 2 0 012-2h4l2 2h6a2 2 0 012 2v1H2V4z" />
          <path d="M2 7h16v7a2 2 0 01-2 2H4a2 2 0 01-2-2V7z" />
        </svg>
        <span className="text-gray-800 font-medium">{folder.name}</span>
      </div>
    </div>
  );
}
