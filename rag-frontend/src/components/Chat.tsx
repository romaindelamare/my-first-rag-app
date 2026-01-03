import { useState, useRef, useEffect } from "react";
import { Send } from "lucide-react";
import { sendChat } from "../api/chat";
import type { SourceChunk, Confidence } from "../models/rag";
import SourcesDrawer from "./SourcesDrawer";

import {
  loadSessionMessages,
  saveSessionMessages,
} from "../utils/sessionManager";
import "highlight.js/styles/github-dark.css";
import { renderMarkdown } from "../utils/markdown";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  rendered?: string;
  sources?: SourceChunk[];
  confidence?: Confidence;
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
    const el = bottomRef.current;
    if (!el) return;

    const isNearBottom =
      window.innerHeight + window.scrollY >= document.body.offsetHeight - 150;

    if (isNearBottom) {
      el.scrollIntoView({ behavior: "smooth" });
    }
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

      // Create an empty assistant message first
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "", rendered: "", sources: response.sources },
      ]);

      await animateAssistantResponse(response.answer, response.confidence, response.sources);

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

  async function animateAssistantResponse(fullText: string, confidence?: Confidence, sources?: SourceChunk[]) {
    let displayed = "";

    for (let i = 0; i < fullText.length; i++) {
      displayed += fullText[i];

      const rendered = await renderMarkdown(displayed);

      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          role: "assistant",
          content: displayed,
          rendered,
          sources,
          confidence
        };
        return updated;
      });

      await new Promise((res) => setTimeout(res, 8)); // typing speed
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
                <div
                  className="prose prose-invert max-w-none whitespace-pre-wrap"
                  dangerouslySetInnerHTML={{ __html: m.rendered || m.content }}
                />

                {m.role === "assistant" && (m.confidence || (m.sources && m.sources.length > 0)) && (
                  <div className="mt-2 flex items-center justify-between gap-4">
                    <div>
                      {m.confidence && (
                        <span
                          className={`inline-block text-xs px-2 py-0.5 rounded-full font-semibold
                            ${
                              m.confidence === "high"
                                ? "bg-green-600/20 text-green-400"
                                : m.confidence === "medium"
                                ? "bg-yellow-600/20 text-yellow-400"
                                : m.confidence === "low"
                                ? "bg-orange-600/20 text-orange-400"
                                : "bg-red-600/20 text-red-400"
                            }
                          `}
                        >
                          Confidence: {m.confidence.toUpperCase()}
                        </span>
                      )}
                    </div>
                    {m.sources && m.sources.length > 0 && (
                      <button
                        className="text-xs text-blue-400 hover:text-blue-300 underline"
                        onClick={() => setDrawerSources(m.sources!)}
                      >
                        View Sources ({m.sources.length})
                      </button>
                    )}
                  </div>
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
