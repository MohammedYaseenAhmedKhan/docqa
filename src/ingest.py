# src/ingest.py

import argparse
import json
from pathlib import Path

import pdfplumber
from docx import Document


def ingest_txt(path: Path):
    pages = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="latin-1")

    pages.append({
        "doc_id": path.stem,
        "source": str(path),
        "page": 1,
        "text": text.strip()
    })
    return pages


def ingest_pdf(path: Path):
    pages = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages.append({
                "doc_id": path.stem,
                "source": str(path),
                "page": i + 1,
                "text": text.strip()
            })
    return pages


def ingest_docx(path: Path):
    doc = Document(path)
    full_text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    return [{
        "doc_id": path.stem,
        "source": str(path),
        "page": 1,
        "text": full_text
    }]


def main(input_dir: str, output_file: str):
    input_path = Path(input_dir)
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    all_pages = []

    for file in input_path.glob("*"):
        if file.suffix.lower() == ".txt":
            all_pages.extend(ingest_txt(file))

        elif file.suffix.lower() == ".pdf":
            all_pages.extend(ingest_pdf(file))

        elif file.suffix.lower() == ".docx":
            all_pages.extend(ingest_docx(file))

    with open(output_path, "w", encoding="utf-8") as f:
        for page in all_pages:
            f.write(json.dumps(page, ensure_ascii=False) + "\n")

    print(f"Ingested {len(all_pages)} pages from {input_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest enterprise documents")
    parser.add_argument("--input", required=True, help="Input data directory")
    parser.add_argument("--out", required=True, help="Output JSONL file")

    args = parser.parse_args()
    main(args.input, args.out)
