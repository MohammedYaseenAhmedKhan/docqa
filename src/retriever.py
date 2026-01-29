# src/retriever.py
import json
import numpy as np
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer


class Retriever:
    def __init__(self):
        print("Loading embedding model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        print("Loading FAISS index...")
        self.index = faiss.read_index("data/faiss.index")

        print("Loading metadata...")
        self.metadata = []
        with open("data/embeddings_meta.jsonl", "r", encoding="utf-8") as f:
            for line in f:
                self.metadata.append(json.loads(line))

    def search(self, query: str, k: int = 3):
        print(f"Searching for: {query}")

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        scores, indices = self.index.search(query_embedding, k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            # Skip FAISS empty slots
            if idx == -1 or score < -1e10:
                continue

            chunk = self.metadata[idx]
            results.append({
                "score": float(score),
                "doc_id": chunk["doc_id"],
                "page": chunk["page"],
                "text": chunk["text"]
            })

        return results


if __name__ == "__main__":
    retriever = Retriever()
    results = retriever.search("What is the leave policy?", k=3)

    for r in results:
        print("\n---")
        print("Score:", r["score"])
        print("Doc:", r["doc_id"], "Page:", r["page"])
        print(r["text"])

