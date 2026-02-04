# src/ingest.py

import argparse
import json
from pathlib import Path

import pdfplumber
from docx import Document


# -------------------------------
# TXT extraction
# -------------------------------
def extract_text_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


# -------------------------------
# PDF extraction
# -------------------------------
def extract_text_pdf(path: str):
    pages = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            if text.strip():
                pages.append({
                    "page": i + 1,
                    "text": text
                })
    return pages


# -------------------------------
# DOCX (Word) extraction
# -------------------------------
def extract_text_docx(path: str) -> str:
    document = Document(path)
    paragraphs = []

    for para in document.paragraphs:
        if para.text.strip():
            paragraphs.append(para.text.strip())

    return "\n".join(paragraphs)


# -------------------------------
# Main ingestion logic
# -------------------------------
def ingest(input_dir: str, output_file: str):
    input_dir = Path(input_dir)
    pages_out = []

    for path in input_dir.glob("**/*"):
        if path.is_dir():
            continue

        suffix = path.suffix.lower()
        doc_id = path.stem

        # TXT
        if suffix == ".txt":
            text = extract_text_txt(str(path))
            pages_out.append({
                "doc_id": doc_id,
                "source": str(path),
                "page": 1,
                "text": text
            })

        # PDF
        elif suffix == ".pdf":
            pages = extract_text_pdf(str(path))
            for p in pages:
                pages_out.append({
                    "doc_id": doc_id,
                    "source": str(path),
                    "page": p["page"],
                    "text": p["text"]
                })

        # DOCX
        elif suffix == ".docx":
            text = extract_text_docx(str(path))
            pages_out.append({
                "doc_id": doc_id,
                "source": str(path),
                "page": 1,
                "text": text
            })

    # Ensure output directory exists
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write JSONL
    with open(output_path, "w", encoding="utf-8") as f:
        for row in pages_out:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Ingested {len(pages_out)} document pages")


# -------------------------------
# CLI entrypoint
# -------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input directory (data/raw)")
    parser.add_argument("--out", default="data/raw_pages.jsonl", help="Output JSONL")
    args = parser.parse_args()

    ingest(args.input, args.out)
