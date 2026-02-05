# src/chunker.py

import json
from pathlib import Path
from sentence_transformers import SentenceTransformer


RAW_PAGES = Path("data/raw_pages.jsonl")
OUTPUT_CHUNKS = Path("data/chunks.jsonl")

MAX_TOKENS = 400
OVERLAP = 80


def chunk_text(text, tokenizer, max_tokens=400, overlap=80):
    tokens = tokenizer.encode(text)
    chunks = []

    start = 0
    while start < len(tokens):
        end = start + max_tokens
        chunk_tokens = tokens[start:end]
        chunk_text = tokenizer.decode(chunk_tokens)

        chunks.append(chunk_text.strip())
        start += max_tokens - overlap

    return chunks


def main():
    tokenizer = SentenceTransformer("all-MiniLM-L6-v2").tokenizer
    OUTPUT_CHUNKS.parent.mkdir(parents=True, exist_ok=True)

    with open(RAW_PAGES, "r", encoding="utf-8") as f:
        pages = [json.loads(line) for line in f]

    total_chunks = 0
    with open(OUTPUT_CHUNKS, "w", encoding="utf-8") as out:
        for page in pages:
            chunks = chunk_text(
                page["text"],
                tokenizer,
                MAX_TOKENS,
                OVERLAP
            )

            for i, chunk in enumerate(chunks):
                out.write(json.dumps({
                    "doc_id": page["doc_id"],
                    "page": page.get("page", 1),
                    "chunk_id": i,
                    "text": chunk
                }, ensure_ascii=False) + "\n")
                total_chunks += 1

    print(f"Created {total_chunks} chunks")


if __name__ == "__main__":
    main()
