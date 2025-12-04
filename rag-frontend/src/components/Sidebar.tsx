import { Plus, Trash2 } from "lucide-react";

interface Props {
  sessions: string[];
  activeSession: string;
  onSelect: (id: string) => void;
  onNew: () => void;
  onDelete: (id: string) => void;
}

export default function Sidebar({
  sessions,
  activeSession,
  onSelect,
  onNew,
  onDelete,
}: Props) {
  return (
    <div className="w-60 bg-neutral-900 border-r border-neutral-800 p-4 flex flex-col h-full">
      <button
        className="mb-4 w-full py-2 bg-blue-600 rounded-xl hover:bg-blue-700"
        onClick={onNew}
      >
        <div className="flex items-center justify-center gap-2">
          <Plus size={18} /> New Chat
        </div>
      </button>

      <div className="flex-1 overflow-y-auto space-y-2">
        {sessions.map((id) => (
          <div
            key={id}
            className={`flex justify-between items-center px-3 py-2 rounded-lg cursor-pointer ${
              id === activeSession
                ? "bg-neutral-700 text-white"
                : "bg-neutral-800 text-neutral-400 hover:bg-neutral-700"
            }`}
            onClick={() => onSelect(id)}
          >
            <span className="truncate">{id}</span>

            <Trash2
              size={16}
              className="hover:text-red-400"
              onClick={(e) => {
                e.stopPropagation();
                onDelete(id);
              }}
            />
          </div>
        ))}

        {sessions.length === 0 && (
          <p className="text-neutral-500 text-sm">No conversations yet</p>
        )}
      </div>
    </div>
  );
}
