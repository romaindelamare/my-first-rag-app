import { useEffect, useState } from "react";
import { listDocuments, deleteDocument, reindexDocument } from "../api/docs";
import { Trash2, RefreshCcw } from "lucide-react";
import UploadBox from "../components/UploadBox";
import { getDocumentChunks } from "../api/docs";
import ChunkDrawer from "../components/ChunkDrawer";

export default function DocumentsPage() {
  const [docs, setDocs] = useState<Record<string, { count: number }>>({});
  const [loading, setLoading] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [selectedDoc, setSelectedDoc] = useState<string | null>(null);
  const [chunks, setChunks] = useState<{ text: string; doc_id: string }[]>([]);


  async function refreshDocs() {
    setLoading(true);
    try {
      const res = await listDocuments();
      setDocs(res.data);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  }

  useEffect(() => {
    let mounted = true;

    async function load() {
        setLoading(true);
        try {
        const res = await listDocuments();
        if (mounted) setDocs(res.data);
        } finally {
        if (mounted) setLoading(false);
        }
    }

    load();

    return () => {
        mounted = false;
    };
    }, []);

  async function handleDelete(docId: string) {
    if (!confirm("Delete this document?")) return;

    await deleteDocument(docId);
    refreshDocs();
  }

  async function handleReindex(docId: string) {
    await reindexDocument(docId);
    refreshDocs();
  }

  async function handleViewChunks(docId: string) {
    setSelectedDoc(docId);
    const res = await getDocumentChunks(docId);
    setChunks(res.data.chunks ?? []);
    setDrawerOpen(true);
  }


  return (
    <div className="min-h-screen bg-neutral-900 text-neutral-100 p-8">
      <h1 className="text-3xl font-semibold mb-6">Documents</h1>

      <div className="mb-8">
        <UploadBox onUploaded={refreshDocs} />
    </div>

      <div className="space-y-4">
        {Object.entries(docs).map(([docId, info]) => (
          <div
            key={docId}
            className="border border-neutral-700 bg-neutral-800 rounded-xl p-4 flex justify-between items-center"
          >
            <div>
              <div className="font-medium">{docId}</div>
              <div className="text-sm text-neutral-400">
                {info.count} chunks
              </div>
            </div>

            <div className="flex gap-3">
              <button
                onClick={() => handleViewChunks(docId)}
                className="p-2 bg-neutral-700 hover:bg-neutral-600 rounded-xl"
              >
                View
              </button>
              
              <button
                onClick={() => handleReindex(docId)}
                className="p-2 bg-blue-600 hover:bg-blue-700 rounded-xl"
              >
                <RefreshCcw size={18} />
              </button>

              <button
                onClick={() => handleDelete(docId)}
                className="p-2 bg-red-600 hover:bg-red-700 rounded-xl"
              >
                <Trash2 size={18} />
              </button>
            </div>
          </div>
        ))}

        {Object.keys(docs).length === 0 && !loading && (
          <div className="text-neutral-400">No documents indexed yet.</div>
        )}
      </div>
      <ChunkDrawer
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        docId={selectedDoc ?? ""}
        chunks={chunks}
      />
    </div>
  );
}
