import argparse
import json
from pathlib import Path
import pdfplumber
import markdown
import re

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()

def ingest_pdf(path: Path):
    pages = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages.append({
                "doc_id": path.stem,
                "source": str(path),
                "page": i + 1,
                "text": clean_text(text)
            })
    return pages

def ingest_markdown_or_txt(path: Path):
    raw = path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix.lower() in {".md", ".markdown"}:
        raw = markdown.markdown(raw)
        raw = re.sub(r"<[^>]+>", "", raw)
    return [{
        "doc_id": path.stem,
        "source": str(path),
        "page": 1,
        "text": clean_text(raw)
    }]

def main(input_dir: str, out_file: str):
    input_dir = Path(input_dir)
    output = []

    for file in input_dir.rglob("*"):
        if file.suffix.lower() == ".pdf":
            output.extend(ingest_pdf(file))
        elif file.suffix.lower() in {".txt", ".md", ".markdown"}:
            output.extend(ingest_markdown_or_txt(file))

    Path(out_file).parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        for row in output:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Ingested {len(output)} pages")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", default="data/raw_pages.jsonl")
    args = parser.parse_args()

    main(args.input, args.out)
