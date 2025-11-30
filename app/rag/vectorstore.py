import faiss
import numpy as np
import json
import os

DB_FOLDER = "db"
META_FILE = os.path.join(DB_FOLDER, "meta.json")
INDEX_FILE = os.path.join(DB_FOLDER, "index.faiss")

def keyword_score(query: str, text: str) -> int:
    """Simple lexical scoring: counts how many query words appear in the chunk."""
    query_words = query.lower().split()
    text_lower = text.lower()

    score = 0
    for w in query_words:
        if w in text_lower:
            score += 1
    return score

class VectorStore:
    def __init__(self, dim=768):
        self.dim = dim

        # Ensure db folder exists
        if not os.path.exists(DB_FOLDER):
            os.makedirs(DB_FOLDER)

        # Load or create index + metadata
        if os.path.exists(INDEX_FILE) and os.path.exists(META_FILE):
            try:
                self.index = faiss.read_index(INDEX_FILE)
                with open(META_FILE, "r") as f:
                    self.meta = json.load(f)
            except Exception:
                # Failed to load → start fresh
                self.index = faiss.IndexFlatL2(self.dim)
                self.meta = []
        else:
            # Fresh DB
            self.index = faiss.IndexFlatL2(self.dim)
            self.meta = []

    def add(self, embedding, text, doc_id):
        embedding = np.array([embedding]).astype("float32")
        self.index.add(embedding)

        self.meta.append({
            "doc_id": doc_id,
            "text": text
        })

    def save(self):
        os.makedirs("db", exist_ok=True)
        faiss.write_index(self.index, INDEX_FILE)
        with open(META_FILE, "w") as f:
            json.dump(self.meta, f)


    def search(self, q_emb, retrieval_k=5, query_text=""):
        # Vector search
        D, I = self.index.search(np.array([q_emb]).astype("float32"), retrieval_k * 3)
        vector_results = [self.meta[i] for i in I[0] if i != -1]

        # Keyword scoring
        scored = []
        for entry in vector_results:
            text = entry["text"]
            kw = keyword_score(query_text, text)
            scored.append((kw, entry))

        # Sort by score
        scored.sort(reverse=True, key=lambda x: x[0])

        # Return metadata dicts (not strings)
        return [entry for score, entry in scored[:retrieval_k]]

