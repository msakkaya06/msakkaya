export default function FileCard({ file }) {
  const getIcon = (ext) => {
    switch (ext) {
      case "pdf":
        return "📕";
      case "jpg":
      case "jpeg":
      case "png":
        return "🖼️";
      case "doc":
      case "docx":
        return "📄";
      case "xls":
      case "xlsx":
        return "📊";
      default:
        return "📁";
    }
  };

  const extension = file.name.split(".").pop().toLowerCase();

  return (
    <a
      href={`http://localhost:9090${file.file}`}
      target="_blank"
      rel="noopener noreferrer"
      className="block border rounded-lg shadow hover:shadow-md p-4 bg-white transition"
    >
      <div className="flex items-center space-x-3">
        <div className="text-xl">{getIcon(extension)}</div>
        <div className="text-gray-800 font-medium truncate">{file.name}</div>
      </div>
    </a>
  );
}
