import API from "./client";

export interface FaissInfo {
  vectors: number;
  dimension: number;
  documents: number;
  index_file_size_bytes: number;
}

export function getFaissInfo() {
  return API.get<FaissInfo>("/faiss/info");
}
