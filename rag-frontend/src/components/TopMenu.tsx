import { Link, useLocation } from "react-router-dom";

export default function TopMenu() {
  const location = useLocation();

  const linkClass = (path: string) =>
    `px-4 py-2 rounded-lg text-sm transition ${
      location.pathname === path
        ? "bg-neutral-700 text-white"
        : "text-neutral-300 hover:bg-neutral-800"
    }`;

  return (
    <div className="w-full bg-neutral-900 border-b border-neutral-800 p-3 flex gap-4">
      <Link to="/chat" className={linkClass("/chat")}>Chat</Link>
      <Link to="/documents" className={linkClass("/documents")}>Documents</Link>
      <Link to="/faiss" className={linkClass("/faiss")}>FAISS Index</Link>
    </div>
  );
}
