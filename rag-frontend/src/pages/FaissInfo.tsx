import { useEffect, useState } from "react";
import { getFaissInfo, type FaissInfo } from "../api/faiss";

export default function FaissInfoPage() {
  const [info, setInfo] = useState<FaissInfo | null>(null);
  const [loading, setLoading] = useState(false);

  async function loadInfo() {
    setLoading(true);
    try {
      const res = await getFaissInfo();
      setInfo(res.data);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadInfo();
  }, []);

  function formatBytes(bytes: number) {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    if (bytes < 1024 * 1024 * 1024) return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
    return `${(bytes / 1024 / 1024 / 1024).toFixed(1)} GB`;
  }

  return (
    <div className="min-h-screen bg-neutral-900 text-neutral-100 p-8">
      <h1 className="text-3xl font-semibold mb-6">FAISS Index</h1>

      {loading && <p className="text-neutral-400">Loading...</p>}

      {info && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          
          <div className="p-6 bg-neutral-800 rounded-xl border border-neutral-700 shadow">
            <h2 className="text-lg font-semibold mb-2">Vectors</h2>
            <p className="text-3xl font-bold text-blue-400">{info.vectors}</p>
            <p className="text-neutral-500 text-sm">
              Total embedded text chunks
            </p>
          </div>

          <div className="p-6 bg-neutral-800 rounded-xl border border-neutral-700 shadow">
            <h2 className="text-lg font-semibold mb-2">Embedding Dimension</h2>
            <p className="text-3xl font-bold text-blue-400">{info.dimension}</p>
            <p className="text-neutral-500 text-sm">
              Dimension of each vector
            </p>
          </div>

          <div className="p-6 bg-neutral-800 rounded-xl border border-neutral-700 shadow">
            <h2 className="text-lg font-semibold mb-2">Documents</h2>
            <p className="text-3xl font-bold text-green-400">{info.documents}</p>
            <p className="text-neutral-500 text-sm">
              Number of indexed documents
            </p>
          </div>

          <div className="p-6 bg-neutral-800 rounded-xl border border-neutral-700 shadow">
            <h2 className="text-lg font-semibold mb-2">Index File Size</h2>
            <p className="text-3xl font-bold text-yellow-400">
              {formatBytes(info.index_file_size_bytes)}
            </p>
            <p className="text-neutral-500 text-sm">
              Size of index.faiss on disk
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
