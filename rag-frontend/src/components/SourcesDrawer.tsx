import { X } from "lucide-react";
import type { SourceChunk } from "../models/rag";

interface Props {
  open: boolean;
  onClose: () => void;
  sources: SourceChunk[];
}

export default function SourcesDrawer({ open, onClose, sources }: Props) {
  if (!open) return null;

  return (
    <div
      className="fixed inset-0 bg-black/40 backdrop-blur-sm flex justify-end"
      onClick={onClose}
    >
      <div
        className="w-full sm:w-[28rem] bg-neutral-900 h-full p-6 overflow-y-auto shadow-xl border-l border-neutral-700"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Sources</h2>
          <button onClick={onClose}>
            <X className="text-neutral-300 hover:text-white" />
          </button>
        </div>

        <div className="space-y-6">
          {sources.map((src, i) => (
            <div
              key={i}
              className="border border-neutral-700 rounded-xl p-4 bg-neutral-800"
            >
              <div className="text-xs text-neutral-400 mb-2">
                Document: {src.doc_id}
              </div>
              <div className="whitespace-pre-line text-sm text-neutral-100">
                {src.text}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
