# src/indexer.py
import numpy as np
import faiss
from pathlib import Path


def main():
    embeddings_path = Path("data/embeddings.npy")
    index_path = Path("data/faiss.index")

    print("Loading embeddings...")
    embeddings = np.load(embeddings_path)

    dim = embeddings.shape[1]
    print("Embedding dimension:", dim)

    # IndexFlatIP = Inner Product (cosine similarity if vectors normalized)
    index = faiss.IndexFlatIP(dim)

    print("Adding embeddings to FAISS index...")
    index.add(embeddings)

    print("Total vectors indexed:", index.ntotal)

    print("Saving FAISS index...")
    faiss.write_index(index, str(index_path))

    print("FAISS index saved successfully")


if __name__ == "__main__":
    main()