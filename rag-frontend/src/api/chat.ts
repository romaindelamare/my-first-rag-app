import API from "./client";
import type { ChatResponse } from "../models/rag";
import type { AxiosError } from "axios";

export async function sendChat(
  sessionId: string,
  userMessage: string
): Promise<ChatResponse> {
  const body = {
    session_id: sessionId,
    messages: [{ role: "user", content: userMessage }],
  };

  try {
    const res = await API.post<ChatResponse>("/chat", body);
    return res.data;
  } catch (err: unknown) {
    if (isAxiosError(err)) {
      const data = err.response?.data;

      if (data && typeof data === "object" && "type" in data) {
        const type = (data as { type: string }).type;
        const message = (data as { message?: string }).message ?? "RAG error";
        if (type === "rag_error") {
          throw new Error(message);
        }
      }

      if (data && typeof data === "object" && "detail" in data) {
        const detail = (data as { detail: string }).detail;
        throw new Error(detail);
      }
    }

    throw new Error("Failed to communicate with the server.");
  }
}

function isAxiosError(error: unknown): error is AxiosError {
  return (
    typeof error === "object" &&
    error !== null &&
    "isAxiosError" in error
  );
}