import API from "./client";
import type { QueryResponse } from "../models/rag";

export async function askQuery(question: string): Promise<QueryResponse> {
  const body = { question };
  const res = await API.post<QueryResponse>("/query", body);
  return res.data;
}
