# src/chunker.py
print(">>> CHUNKER FILE EXECUTED <<<", flush=True)

import json
from pathlib import Path
import re


def count_tokens(text: str) -> int:
    # Approx: 1 token ≈ 4 characters
    return max(1, len(text) // 4)


def chunk_text(text: str, max_tokens: int = 300, overlap_tokens: int = 50):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks = []
    current_chunk = ""
    current_tokens = 0

    for sent in sentences:
        sent_tokens = count_tokens(sent)

        if current_tokens + sent_tokens > max_tokens:
            chunks.append(current_chunk.strip())

            # overlap
            overlap_text = current_chunk[-overlap_tokens * 4 :]
            current_chunk = overlap_text + " " + sent
            current_tokens = count_tokens(current_chunk)
        else:
            current_chunk += " " + sent
            current_tokens += sent_tokens

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def main():
    print(">>> ENTERED MAIN()", flush=True)

    input_path = Path("data/raw_pages.jsonl")
    output_path = Path("data/chunks.jsonl")

    print("Reading from:", input_path, flush=True)

    chunk_rows = []
    chunk_id = 0

    with input_path.open("r", encoding="utf-8") as f:
        for line in f:
            print(">>> RAW LINE FOUND", flush=True)
            row = json.loads(line)

            print("Processing doc:", row["doc_id"], flush=True)

            text = row["text"]
            chunks = chunk_text(text)

            for chunk in chunks:
                chunk_rows.append({
                    "chunk_id": chunk_id,
                    "doc_id": row["doc_id"],
                    "page": row["page"],
                    "text": chunk
                })
                chunk_id += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        for row in chunk_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print("Created", len(chunk_rows), "chunks", flush=True)


if __name__ == "__main__":
    main()
