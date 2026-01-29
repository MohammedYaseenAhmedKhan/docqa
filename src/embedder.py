# src/embedder.py
import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer


def load_chunks(path: str):
    chunks = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))
    return chunks


def main():
    input_path = Path("data/chunks.jsonl")
    output_vectors = Path("data/embeddings.npy")
    output_meta = Path("data/embeddings_meta.jsonl")

    print("Loading chunks...")
    chunks = load_chunks(input_path)
    texts = [c["text"] for c in chunks]

    print(f"Loaded {len(texts)} chunks")

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Generating embeddings...")
    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    print("Saving embeddings...")
    np.save(output_vectors, embeddings)

    print("Saving metadata...")
    with open(output_meta, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print("Embeddings saved successfully")
    print("Vector shape:", embeddings.shape)


if __name__ == "__main__":
    main()
