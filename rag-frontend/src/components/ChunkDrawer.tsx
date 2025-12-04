import { X } from "lucide-react";

interface Chunk {
  text: string;
  doc_id: string;
}

interface Props {
  open: boolean;
  onClose: () => void;
  docId: string;
  chunks: Chunk[];
}

export default function ChunkDrawer({ open, onClose, docId, chunks }: Props) {
  if (!open) return null;

  return (
    <div
      className="fixed inset-0 bg-black/40 backdrop-blur-sm flex justify-end"
      onClick={onClose}
    >
      <div
        className="w-full sm:w-[32rem] bg-neutral-900 h-full p-6 overflow-y-auto shadow-xl border-l border-neutral-700"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold">Chunks for {docId}</h2>
          <button onClick={onClose}>
            <X className="text-neutral-300 hover:text-white" />
          </button>
        </div>

        <div className="space-y-6">
          {chunks.map((chunk, index) => (
            <div
              key={index}
              className="border border-neutral-700 rounded-xl p-4 bg-neutral-800"
            >
              <div className="text-xs text-neutral-400 mb-2">
                Chunk {index + 1}
              </div>
              <div className="whitespace-pre-line text-sm text-neutral-100">
                {chunk.text}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
