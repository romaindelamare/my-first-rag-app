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

export interface HallucinationResult {
  score: number;
  hallucinated: boolean;
}

export interface SemanticScore {
  chunk_scores: number[];
  average: number;
  max: number;
  min: number;
  confidence: "low" | "medium" | "high";
}

export interface Citation {
  sentence: string;
  source_doc_id: string | null;
  score: number;
}

export interface SafetyResult {
  safe: boolean;
  category: string | null;
  score: number;
}

export interface Decision {
  allowed: boolean;
  reason: string | null;
  final_answer: string;
}

export interface ChatResponse {
  answer: string;
  sources: SourceChunk[];
  memory_context: string;
}

export interface QueryResponse {
  answer: string;
  sources: SourceChunk[];
  evaluation: Evaluation;
  hallucination: HallucinationResult;
  semantic: SemanticScore;
  citations: Citation[];
  safety: SafetyResult;
  decision: Decision;
}

export interface Evaluation {
    overlap_score: string;
    source_count: string;
    confidence: string;
}