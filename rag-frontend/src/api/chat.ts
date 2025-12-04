import API from "./client";
import type { ChatResponse } from "../models/rag";

export async function sendChat(
  sessionId: string,
  userMessage: string
): Promise<ChatResponse> {
  const body = {
    session_id: sessionId,
    messages: [{ role: "user", content: userMessage }],
  };

  const res = await API.post<ChatResponse>("/chat", body);
  return res.data;
}
