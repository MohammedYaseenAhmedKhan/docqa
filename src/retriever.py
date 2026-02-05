# src/retriever.py
import json
import faiss
import numpy as np
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

        print(f"Loaded {len(self.metadata)} document chunks")

    def search(self, query: str, k: int = 5):
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        scores, indices = self.index.search(query_embedding, 10)

        results = []
        query_lower = query.lower()

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            chunk = self.metadata[idx]

            # 🔹 Bias scoring using document name
            doc_bonus = 0.0
            if chunk["doc_id"].lower() in query_lower:
                doc_bonus = 0.15

            final_score = float(score) + doc_bonus

            results.append({
                "score": final_score,
                "doc_id": chunk["doc_id"],
                "page": chunk["page"],
                "text": chunk["text"]
            })

        # 🔹 Sort by adjusted score
        results = sorted(results, key=lambda x: x["score"], reverse=True)

        return results[:k]


def interactive_mode():
    retriever = Retriever()

    print("\nSemantic Retriever Ready")
    print("Ask questions about enterprise policies.")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Ask a question: ").strip()
        if query.lower() == "exit":
            break

        results = retriever.search(query)

        for r in results:
            print("\n---")
            print(f"Score: {r['score']:.4f}")
            print(f"Doc: {r['doc_id']} | Page: {r['page']}")
            print(r["text"])


if __name__ == "__main__":
    interactive_mode()
