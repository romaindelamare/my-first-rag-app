import API from "./client";

export function listDocuments() {
  return API.get<Record<string, { count: number }>>("/documents");
}

export function getDocument(docId: string) {
  return API.get(`/documents/${docId}`);
}

export function deleteDocument(docId: string) {
  return API.delete(`/documents/${docId}`);
}

export function reindexDocument(docId: string) {
  return API.post(`/documents/${docId}/reindex`);
}

export function uploadDocument(form: FormData) {
  return API.post("/upload", form, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
}

export async function getDocumentChunks(docId: string) {
  return API.get<{ chunks: { text: string; doc_id: string }[] }>(
    `/documents/${docId}`
  );
}