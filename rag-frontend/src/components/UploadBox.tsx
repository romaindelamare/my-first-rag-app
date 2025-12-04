import { useState, type DragEvent, type ChangeEvent } from "react";
import { uploadDocument } from "../api/docs";
import { UploadCloud } from "lucide-react";

interface Props {
  onUploaded: () => void;
}

export default function UploadBox({ onUploaded }: Props) {
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);

  function handleDrag(e: DragEvent<HTMLDivElement>) {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }

  async function handleFile(file: File) {
    if (!file) return;

    setFileName(file.name);
    setUploading(true);

    try {
      const form = new FormData();
      form.append("file", file);

      await uploadDocument(form);
      onUploaded();
    } catch (err) {
      console.error(err);
    }

    setUploading(false);
    setDragActive(false);
  }

  function handleDrop(e: DragEvent<HTMLDivElement>) {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const file = e.dataTransfer.files?.[0];
    if (file) handleFile(file);
  }

  function handleChange(e: ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  }

  return (
    <div
      className={`border-2 border-dashed rounded-xl p-10 text-center transition 
        ${
          dragActive
            ? "border-blue-500 bg-blue-500/10"
            : "border-neutral-700 bg-neutral-800"
        }`}
      onDragEnter={handleDrag}
      onDragOver={handleDrag}
      onDragLeave={handleDrag}
      onDrop={handleDrop}
    >
      {uploading ? (
        <div className="text-neutral-300 flex flex-col items-center gap-3">
          <div className="animate-spin text-blue-400">
            <UploadCloud size={40} />
          </div>
          <div>Uploading <span className="font-medium">{fileName}</span>...</div>
        </div>
      ) : (
        <>
          <div className="flex justify-center mb-4">
            <UploadCloud size={40} className="text-neutral-400" />
          </div>

          <p className="text-neutral-300">
            Drag & drop a file here, or{" "}
            <label className="text-blue-400 hover:text-blue-300 cursor-pointer underline">
              click to upload
              <input
                type="file"
                className="hidden"
                onChange={handleChange}
                accept=".txt,.md,.pdf,.json"
              />
            </label>
          </p>

          <p className="text-neutral-500 text-xs mt-3">
            Supported: TXT, Markdown, PDF, JSON
          </p>
        </>
      )}
    </div>
  );
}
