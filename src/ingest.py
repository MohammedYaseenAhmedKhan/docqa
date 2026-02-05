import argparse
import json
from pathlib import Path

import pdfplumber
from docx import Document


def normalize_doc_id(path: Path) -> str:
    return path.stem.replace("_", " ").replace("-", " ").title()


def read_txt(path):
    return path.read_text(encoding="utf-8", errors="ignore")


def read_pdf(path):
    text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)


def read_docx(path):
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


def ingest(input_dir: Path, output_file: Path):
    records = []

    for file in input_dir.iterdir():
        if file.suffix.lower() not in [".txt", ".pdf", ".docx"]:
            continue

        doc_id = normalize_doc_id(file)

        if file.suffix == ".txt":
            text = read_txt(file)
        elif file.suffix == ".pdf":
            text = read_pdf(file)
        else:
            text = read_docx(file)

        if not text.strip():
            continue

        records.append({
            "doc_id": doc_id,
            "page": 1,
            "text": text.strip()
        })

    with open(output_file, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Ingested {len(records)} documents")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    ingest(Path(args.input), Path(args.out))
