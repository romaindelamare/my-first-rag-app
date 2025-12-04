import type { SourceChunk } from "../models/rag";

export interface StoredMessage {
  role: "user" | "assistant";
  content: string;
  sources?: SourceChunk[];
}

const SESSION_KEY = "sessions";

export function getSessions(): string[] {
  const raw = localStorage.getItem(SESSION_KEY);
  return raw ? JSON.parse(raw) : [];
}

export function saveSessions(sessions: string[]) {
  localStorage.setItem(SESSION_KEY, JSON.stringify(sessions));
}

export function createSession(): string {
  const id = `session-${Date.now()}`;
  const sessions = getSessions();
  sessions.unshift(id);
  saveSessions(sessions);
  localStorage.setItem(`session:${id}`, JSON.stringify([]));
  return id;
}

export function deleteSession(id: string) {
  const sessions = getSessions().filter((s) => s !== id);
  saveSessions(sessions);
  localStorage.removeItem(`session:${id}`);
}

export function loadSessionMessages(id: string): StoredMessage[] {
  const raw = localStorage.getItem(`session:${id}`);
  return raw ? JSON.parse(raw) : [];
}

export function saveSessionMessages(id: string, messages: StoredMessage[]) {
  localStorage.setItem(`session:${id}`, JSON.stringify(messages));
}
