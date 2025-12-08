import { X, Copy } from "lucide-react";
import type { DocumentChunk } from "../models/rag";

interface Props {
  open: boolean;
  onClose: () => void;
  docId: string;
  chunks: DocumentChunk[];
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
          <div>
            <h2 className="text-xl font-semibold">Document Chunks</h2>
            <p className="text-xs text-neutral-500">doc_id: {docId}</p>
          </div>

          <button onClick={onClose}>
            <X className="text-neutral-300 hover:text-white" />
          </button>
        </div>

        <div className="space-y-6">
          {chunks.map((chunk) => {
            const length = chunk.text.length;
            const wordCount = chunk.text.trim().split(/\s+/).length;

            return (
              <div
                key={chunk.chunk_index}
                className="border border-neutral-700 rounded-xl p-4 bg-neutral-800"
              >
                <div className="flex justify-between items-center mb-2">
                  <div className="text-xs text-neutral-400">
                    <strong className="text-neutral-300">
                      Chunk {chunk.chunk_index + 1}
                    </strong>
                    <br />
                    Offset: {chunk.offset_start} → {chunk.offset_end}
                    <br />
                    Length: {length} chars • {wordCount} words
                  </div>

                  <button
                    className="p-1 rounded hover:bg-neutral-700"
                    onClick={() => navigator.clipboard.writeText(chunk.text)}
                  >
                    <Copy size={16} className="text-neutral-300" />
                  </button>
                </div>

                <pre className="whitespace-pre-wrap text-sm text-neutral-100 font-mono leading-relaxed">
                  {chunk.text}
                </pre>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
