export interface SourceChunk {
  doc_id: string;
  text: string;
}

export interface DocumentChunk {
  doc_id: string;
  chunk_index: number;
  text: string;
  offset_start: number;
  offset_end: number;
}

export interface ChatResponse {
  answer: string;
  allowed: boolean;
  reason: string | null;
  confidence?: Confidence;
  sources: SourceChunk[];
}

export type Confidence = "high" | "medium" | "low" | "blocked";