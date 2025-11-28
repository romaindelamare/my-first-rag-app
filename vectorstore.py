import faiss
import numpy as np
import json
import os

class VectorStore:
    def __init__(self, dim, index_path="db/index.faiss", meta_path="db/meta.json"):
        self.dim = dim
        self.index_path = index_path
        self.meta_path = meta_path

        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
            with open(meta_path, "r") as f:
                self.metadata = json.load(f)
        else:
            self.index = faiss.IndexFlatL2(dim)
            self.metadata = []

    def add(self, embedding, text):
        self.index.add(np.array([embedding]).astype("float32"))
        self.metadata.append(text)

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "w") as f:
            json.dump(self.metadata, f)

    def search(self, embedding, top_k=5):
        D, I = self.index.search(np.array([embedding]).astype("float32"), top_k)
        return [self.metadata[i] for i in I[0]]