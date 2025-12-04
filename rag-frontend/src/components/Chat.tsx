import { useState, useRef, useEffect } from "react";
import { Send } from "lucide-react";
import { sendChat } from "../api/chat";
import type { SourceChunk } from "../models/rag";
import SourcesDrawer from "./SourcesDrawer";

import {
  loadSessionMessages,
  saveSessionMessages,
} from "../utils/sessionManager";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  sources?: SourceChunk[];
}

interface Props {
  sessionId: string;
}

export default function Chat({ sessionId }: Props) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loaded, setLoaded] = useState(false);
  const [input, setInput] = useState("");
  const [drawerSources, setDrawerSources] = useState<SourceChunk[] | null>(null);
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    setLoaded(false);

    Promise.resolve().then(() => {
      const stored = loadSessionMessages(sessionId);
      setMessages(stored ?? []);
      setLoaded(true);
    });
  }, [sessionId]);

  useEffect(() => {
    if (!loaded) return;
    saveSessionMessages(sessionId, messages);
  }, [messages, sessionId, loaded]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend() {
    if (!input.trim()) return;

    const userMessage: ChatMessage = {
      role: "user",
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    const userInput = input;
    setInput("");

    try {
      const response = await sendChat(sessionId, userInput);

      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: response.answer,
        sources: response.sources,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "⚠️ Error communicating with backend.",
        },
      ]);
    }
  }

  return (
    <div className="h-full bg-neutral-900 text-neutral-100 flex flex-col">

      <div className="flex-1 overflow-y-auto flex justify-center px-4">
        <div className="w-full max-w-3xl py-6 space-y-6">

          {messages.map((m, i) => (
            <div
              key={i}
              className={`flex ${
                m.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[75%] px-4 py-3 rounded-2xl shadow-md text-sm leading-relaxed
                  ${
                    m.role === "user"
                      ? "bg-blue-600 text-white rounded-br-none"
                      : "bg-neutral-800 text-neutral-100 rounded-bl-none"
                  }
                `}
              >
                {m.content}

                {m.sources && m.sources.length > 0 && (
                  <button
                    className="text-xs text-blue-400 hover:text-blue-300 mt-2 underline"
                    onClick={() => setDrawerSources(m.sources!)}
                  >
                    View Sources ({m.sources.length})
                  </button>
                )}
              </div>
            </div>
          ))}

          <div ref={bottomRef} />
        </div>
      </div>

      <div className="border-t border-neutral-700 bg-neutral-900 p-4 flex justify-center">
        <div className="w-full max-w-3xl flex gap-3">
          <input
            className="flex-1 bg-neutral-800 border border-neutral-700 rounded-xl p-3 text-sm text-neutral-100 placeholder-neutral-500
              focus:outline-none focus:ring-2 focus:ring-blue-600"
            placeholder="Ask something..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />

          <button
            className="bg-blue-600 hover:bg-blue-700 transition text-white px-5 py-2 rounded-xl flex items-center gap-2 shadow-md"
            onClick={handleSend}
          >
            <Send size={18} />
            Send
          </button>
        </div>
      </div>

      <SourcesDrawer
        open={drawerSources !== null}
        onClose={() => setDrawerSources(null)}
        sources={drawerSources ?? []}
      />
    </div>
  );
}
